import mimetypes
import time
import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile

from api.core.config import get_settings


def _resource_type(content_type: str) -> str:
    if content_type.startswith("image/"):
        return "image"
    if content_type.startswith("video/"):
        return "video"
    return "raw"


def _validate_file(file: UploadFile, content: bytes) -> tuple[str, str]:
    settings = get_settings()
    filename = Path(file.filename or "attachment").name
    content_type = (file.content_type or "").lower()

    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    if content_type not in settings.allowed_mime_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}",
        )

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds the {settings.max_upload_size_mb}MB limit",
        )

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    return filename, content_type


def _cloudinary_config():
    import cloudinary

    settings = get_settings()
    if not settings.cloudinary_configured:
        raise HTTPException(
            status_code=503,
            detail="Cloudinary storage is not configured",
        )
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )
    return cloudinary


def _upload_to_cloudinary(
    ticket_id: str,
    filename: str,
    content_type: str,
    content: bytes,
) -> dict:
    import cloudinary.uploader

    cloudinary_module = _cloudinary_config()
    settings = get_settings()
    resource_type = _resource_type(content_type)

    result = cloudinary_module.uploader.upload(
        content,
        folder=f"{settings.cloudinary_folder}/tickets/{ticket_id}",
        resource_type=resource_type,
        type="private",
        use_filename=True,
        unique_filename=True,
        filename_override=filename,
        overwrite=False,
    )

    return {
        "file_path": result.get("secure_url", ""),
        "storage_public_id": result.get("public_id"),
        "resource_type": result.get("resource_type", resource_type),
        "original_filename": filename,
        "content_type": content_type,
        "file_size": len(content),
    }


def _upload_to_local(
    ticket_id: str,
    filename: str,
    content_type: str,
    content: bytes,
) -> dict:
    settings = get_settings()
    directory = Path(settings.upload_dir) / "tickets" / str(ticket_id)
    directory.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4().hex}_{filename}"
    path = directory / stored_name
    path.write_bytes(content)

    return {
        "file_path": str(path),
        "storage_public_id": str(path),
        "resource_type": "local",
        "original_filename": filename,
        "content_type": content_type,
        "file_size": len(content),
    }


def save_upload(file: UploadFile, ticket_id) -> dict:
    settings = get_settings()
    content = file.file.read()
    filename, content_type = _validate_file(file, content)

    if settings.storage_backend == "local":
        return _upload_to_local(str(ticket_id), filename, content_type, content)

    return _upload_to_cloudinary(
        str(ticket_id), filename, content_type, content
    )


def get_download_url(
    storage_public_id: Optional[str],
    resource_type: Optional[str],
) -> Optional[str]:
    if not storage_public_id:
        return None
    if resource_type == "local":
        return None

    from cloudinary.utils import cloudinary_url

    _cloudinary_config()
    settings = get_settings()
    expires_at = int(time.time()) + settings.cloudinary_private_download_ttl

    url, _ = cloudinary_url(
        storage_public_id,
        type="private",
        resource_type=resource_type or "image",
        sign_url=True,
        secure=True,
        expires_at=expires_at,
    )
    return url


def delete_file(storage_public_id: Optional[str], resource_type: Optional[str]) -> None:
    if not storage_public_id:
        return

    if resource_type == "local":
        path = Path(storage_public_id)
        if path.exists():
            path.unlink()
        return

    import cloudinary.uploader

    _cloudinary_config()
    cloudinary.uploader.destroy(
        storage_public_id,
        resource_type=resource_type or "image",
        type="private",
        invalidate=True,
    )


def get_local_file_path(attachment) -> Optional[Path]:
    if attachment.resource_type != "local":
        return None
    path = Path(attachment.storage_public_id or attachment.file_path)
    return path if path.exists() else None
