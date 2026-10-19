import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import ValidationError
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, selectinload

from api.core.dependencies import get_current_user
from api.db.database import get_db
from api.utils.email import send_email
from api.utils.file_storage import (
    delete_file,
    get_download_url,
    get_local_file_path,
    save_upload,
)
from api.v1.models.attachement import Attachment
from api.v1.models.comment import Comment
from api.v1.models.history import TicketHistory
from api.v1.models.ticket import Ticket
from api.v1.models.user import User
from api.v1.schemas.tickets import (
    AttachmentResponse,
    CommentCreate,
    TicketAssign,
    TicketCreate,
    TicketHistoryResponse,
    TicketResponse,
    TicketUpdate,
)
from api.v1.services.tickets import (
    ensure_can_view_ticket,
    format_display_name,
    get_ticket_or_404,
    record_history,
)

tickets = APIRouter(prefix="/tickets", tags=["Tickets"])

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}
ALLOWED_TRANSITIONS = {
    "open": {"in_progress", "resolved", "closed"},
    "in_progress": {"open", "resolved", "closed"},
    "resolved": {"in_progress", "closed"},
    "closed": {"open", "in_progress"},
}


def _ticket_query(db: Session):
    return db.query(Ticket).options(
        joinedload(Ticket.created_by_user),
        joinedload(Ticket.assigned_to_user),
        joinedload(Ticket.closed_by_user),
        selectinload(Ticket.attachments),
        selectinload(Ticket.tags),
    )


def _load_ticket(db: Session, ticket_id: UUID) -> Optional[Ticket]:
    return _ticket_query(db).filter(Ticket.id == ticket_id).first()


def _apply_filters(
    query,
    ticket_status: Optional[str],
    priority: Optional[str],
    category: Optional[str],
    search: Optional[str],
):
    if ticket_status:
        query = query.filter(Ticket.status == ticket_status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if category:
        query = query.filter(Ticket.category == category)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(Ticket.subject.ilike(term), Ticket.description.ilike(term))
        )
    return query


def _validate_priority(priority: str) -> str:
    priority = priority.lower()
    if priority not in VALID_PRIORITIES:
        raise HTTPException(
            status_code=400,
            detail=f"Priority must be one of: {', '.join(sorted(VALID_PRIORITIES))}",
        )
    return priority


def _validate_status(ticket_status: str) -> str:
    ticket_status = ticket_status.lower()
    if ticket_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}",
        )
    return ticket_status


def _change_status(ticket: Ticket, new_status: str, user_id: UUID) -> Optional[str]:
    old_status = ticket.status
    if old_status == new_status:
        return None

    now = datetime.utcnow()
    ticket.status = new_status

    if new_status == "resolved":
        ticket.date_resolved = ticket.date_resolved or now
    elif new_status == "closed":
        ticket.date_closed = now
        ticket.closed_by = user_id
    else:
        ticket.date_closed = None
        ticket.closed_by = None
        if new_status == "open":
            ticket.date_resolved = None

    return f"Status changed from {old_status} to {new_status}"


def _validate_support_assignee(db: Session, assigned_to: UUID) -> User:
    assigned_user = db.query(User).filter(User.user_id == assigned_to).first()
    if not assigned_user or assigned_user.role != "support" or not assigned_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Tickets can only be assigned to active support staff",
        )
    return assigned_user


@tickets.post("/", response_model=TicketResponse)
def create_ticket(
    background_tasks: BackgroundTasks,
    ticket_data: str = Form(...),
    attachments: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        payload = TicketCreate(**json.loads(ticket_data))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=400, detail=f"Invalid ticket data: {exc}"
        ) from exc

    priority = _validate_priority(payload.priority or "low")
    ticket_id = uuid.uuid4()
    ticket = Ticket(
        id=ticket_id,
        subject=payload.subject.strip(),
        description=payload.description.strip(),
        category=payload.category.strip(),
        priority=priority,
        assigned_by=None if current_user.role == "student" else current_user.user_id,
        created_by=current_user.user_id,
        date_created=datetime.utcnow(),
        status="open",
    )

    uploaded_attachments = []
    try:
        for file in attachments or []:
            uploaded_attachments.append(save_upload(file, ticket_id))
    except Exception:
        for metadata in uploaded_attachments:
            delete_file(
                metadata.get("storage_public_id"),
                metadata.get("resource_type"),
            )
        raise

    db.add(ticket)
    for metadata in uploaded_attachments:
        db.add(Attachment(ticket_id=ticket_id, **metadata))
    record_history(
        db,
        ticket_id,
        current_user.user_id,
        "Ticket created",
    )
    db.commit()

    reloaded_ticket = _load_ticket(db, ticket_id)
    background_tasks.add_task(
        send_email,
        f"Ticket created: {ticket.subject}",
        [current_user.email],
        (
            f"Your ticket has been created successfully.\n\n"
            f"Ticket ID: {ticket.id}\nSubject: {ticket.subject}\n"
            f"Status: {ticket.status}\nPriority: {ticket.priority}\n"
        ),
    )
    return reloaded_ticket


@tickets.get("/assigned", response_model=List[TicketResponse])
def get_assigned_tickets(
    ticket_status: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "support":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only support staff can view assigned tickets.",
        )

    query = _ticket_query(db).filter(Ticket.assigned_to == current_user.user_id)
    query = _apply_filters(query, ticket_status, priority, category, search)
    return (
        query.order_by(Ticket.date_created.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@tickets.get("/all", response_model=List[TicketResponse])
def get_all_tickets(
    ticket_status: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    assigned_to: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only admins can view all tickets.",
        )

    query = _ticket_query(db)
    if assigned_to:
        query = query.filter(Ticket.assigned_to == assigned_to)
    query = _apply_filters(query, ticket_status, priority, category, search)
    return (
        query.order_by(Ticket.date_created.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@tickets.get("/submitted", response_model=List[TicketResponse])
def get_user_submitted_tickets(
    ticket_status: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = _ticket_query(db).filter(Ticket.created_by == current_user.user_id)
    query = _apply_filters(query, ticket_status, priority, category, search)
    return (
        query.order_by(Ticket.date_created.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@tickets.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    ensure_can_view_ticket(current_user, ticket)
    return ticket


@tickets.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    updates = {
        key: value
        for key, value in ticket_data.model_dump(exclude_unset=True).items()
        if value is not None
    }
    if not updates:
        return ticket

    changes = []
    new_assignee = updates.pop("assigned_to", None)
    new_status = updates.pop("status", None)

    if current_user.role == "admin":
        if new_assignee is not None and new_assignee != ticket.assigned_to:
            assigned_user = _validate_support_assignee(db, new_assignee)
            ticket.assigned_to = new_assignee
            ticket.assigned_by = current_user.user_id
            changes.append(
                f"Assigned to {format_display_name(assigned_user)}"
            )
            if ticket.status == "open":
                status_change = _change_status(
                    ticket, "in_progress", current_user.user_id
                )
                if status_change:
                    changes.append(status_change)

        if new_status is not None:
            new_status = _validate_status(new_status)
            status_change = _change_status(
                ticket, new_status, current_user.user_id
            )
            if status_change:
                changes.append(status_change)

    elif current_user.role == "support":
        if ticket.assigned_to != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update tickets assigned to you",
            )
        if new_assignee is not None:
            raise HTTPException(
                status_code=403,
                detail="Only admins can reassign tickets",
            )
        if new_status is not None:
            new_status = _validate_status(new_status)
            if new_status != ticket.status and new_status not in ALLOWED_TRANSITIONS.get(
                ticket.status, set()
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot change status from {ticket.status} to {new_status}",
                )
            status_change = _change_status(
                ticket, new_status, current_user.user_id
            )
            if status_change:
                changes.append(status_change)
        allowed_updates = {"priority", "category", "description"}
        forbidden = set(updates.keys()) - allowed_updates
        if forbidden:
            raise HTTPException(
                status_code=403,
                detail=f"Support staff cannot update: {', '.join(sorted(forbidden))}",
            )

    else:
        if ticket.created_by != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to update this ticket",
            )
        if ticket.status == "closed":
            raise HTTPException(
                status_code=400, detail="Closed tickets cannot be edited"
            )
        forbidden = set(updates.keys()) - {"subject", "description"}
        if forbidden:
            raise HTTPException(
                status_code=403,
                detail=f"Students cannot update: {', '.join(sorted(forbidden))}",
            )

    if "priority" in updates:
        priority = _validate_priority(updates["priority"])
        if ticket.priority != priority:
            changes.append(
                f"Priority changed from {ticket.priority} to {priority}"
            )
            ticket.priority = priority

    if "category" in updates and ticket.category != updates["category"]:
        changes.append(
            f"Category changed from {ticket.category} to {updates['category']}"
        )
        ticket.category = updates["category"]

    if "subject" in updates and ticket.subject != updates["subject"]:
        changes.append("Subject updated")
        ticket.subject = updates["subject"].strip()

    if "description" in updates and ticket.description != updates["description"]:
        changes.append("Description updated")
        ticket.description = updates["description"]

    for action in changes:
        record_history(db, ticket.id, current_user.user_id, action)

    db.commit()

    if new_status in {"resolved", "closed"}:
        background_tasks.add_task(
            send_email,
            f"Ticket {new_status}: {ticket.subject}",
            [ticket.created_by_user.email],
            (
                f"Your ticket has been marked {new_status}.\n\n"
                f"Ticket ID: {ticket.id}\nSubject: {ticket.subject}\n"
                f"Status: {ticket.status}\n"
            ),
        )

    return _load_ticket(db, ticket_id)


@tickets.put("/{ticket_id}/assign", response_model=Dict[str, Any])
def assign_ticket(
    ticket_id: UUID,
    assign_data: TicketAssign,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can assign tickets")

    ticket = get_ticket_or_404(db, ticket_id)
    assigned_user = _validate_support_assignee(db, assign_data.assigned_to)

    ticket.assigned_to = assign_data.assigned_to
    ticket.assigned_by = current_user.user_id
    changes = [f"Assigned to {format_display_name(assigned_user)}"]

    if ticket.status == "open":
        status_change = _change_status(ticket, "in_progress", current_user.user_id)
        if status_change:
            changes.append(status_change)

    for action in changes:
        record_history(db, ticket.id, current_user.user_id, action)
    db.commit()

    refreshed_ticket = _load_ticket(db, ticket_id)
    background_tasks.add_task(
        send_email,
        f"Ticket assigned: {ticket.subject}",
        [assigned_user.email],
        (
            f"A ticket has been assigned to you.\n\n"
            f"Ticket ID: {ticket.id}\nSubject: {ticket.subject}\n"
            f"Priority: {ticket.priority}\nStatus: {ticket.status}\n"
        ),
    )

    return {
        "message": (
            f"Ticket successfully assigned to "
            f"{format_display_name(assigned_user)} (Support Staff)."
        ),
        "ticket": TicketResponse.model_validate(refreshed_ticket),
    }


@tickets.put("/{ticket_id}/cancel", response_model=TicketResponse)
def cancel_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)

    if current_user.role != "admin" and ticket.created_by != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to cancel this ticket",
        )

    if ticket.status in {"closed"}:
        raise HTTPException(
            status_code=400, detail="Ticket is already cancelled or closed"
        )

    _change_status(ticket, "closed", current_user.user_id)
    record_history(db, ticket.id, current_user.user_id, "Ticket cancelled")
    db.commit()
    db.refresh(ticket)
    return ticket


@tickets.get(
    "/{ticket_id}/attachments",
    response_model=List[AttachmentResponse],
)
def get_ticket_attachments(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    ensure_can_view_ticket(current_user, ticket)

    response = []
    for attachment in ticket.attachments:
        download_url = get_download_url(
            attachment.storage_public_id,
            attachment.resource_type,
        )
        if attachment.resource_type == "local":
            download_url = (
                f"/api/v1/tickets/{ticket_id}/attachments/{attachment.id}/download"
            )
        response.append(
            AttachmentResponse(
                id=attachment.id,
                original_filename=attachment.original_filename,
                content_type=attachment.content_type,
                file_size=attachment.file_size,
                resource_type=attachment.resource_type,
                uploaded_at=attachment.uploaded_at,
                download_url=download_url,
            )
        )
    return response


@tickets.get("/{ticket_id}/attachments/{attachment_id}/download")
def download_attachment(
    ticket_id: UUID,
    attachment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    ensure_can_view_ticket(current_user, ticket)

    attachment = (
        db.query(Attachment)
        .filter(
            Attachment.id == attachment_id,
            Attachment.ticket_id == ticket_id,
        )
        .first()
    )
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    local_path = get_local_file_path(attachment)
    if local_path:
        return FileResponse(
            path=local_path,
            filename=attachment.original_filename or local_path.name,
            media_type=attachment.content_type or "application/octet-stream",
        )

    download_url = get_download_url(
        attachment.storage_public_id,
        attachment.resource_type,
    )
    if not download_url:
        raise HTTPException(status_code=404, detail="Attachment file not found")
    return RedirectResponse(download_url)


@tickets.delete("/{ticket_id}/attachments/{attachment_id}")
def delete_attachment(
    ticket_id: UUID,
    attachment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    if current_user.role != "admin" and ticket.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    attachment = (
        db.query(Attachment)
        .filter(
            Attachment.id == attachment_id,
            Attachment.ticket_id == ticket_id,
        )
        .first()
    )
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    delete_file(attachment.storage_public_id, attachment.resource_type)
    db.delete(attachment)
    record_history(
        db,
        ticket.id,
        current_user.user_id,
        f"Attachment removed: {attachment.original_filename or attachment.id}",
    )
    db.commit()
    return {"message": "Attachment deleted"}


@tickets.post("/{ticket_id}/comments", status_code=201)
def add_comment(
    ticket_id: UUID,
    comment_data: CommentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    if (
        current_user.role != "admin"
        and current_user.user_id != ticket.assigned_to
        and current_user.user_id != ticket.created_by
    ):
        raise HTTPException(
            status_code=403, detail="You do not have access to this ticket"
        )

    comment = Comment(
        id=uuid.uuid4(),
        ticket_id=ticket_id,
        user_id=current_user.user_id,
        message=comment_data.message.strip(),
        timestamp=datetime.utcnow(),
    )
    db.add(comment)
    record_history(db, ticket_id, current_user.user_id, "Comment added")
    db.commit()
    db.refresh(comment)

    recipients = []
    if current_user.user_id == ticket.created_by and ticket.assigned_to_user:
        recipients.append(ticket.assigned_to_user.email)
    elif ticket.created_by_user:
        recipients.append(ticket.created_by_user.email)

    background_tasks.add_task(
        send_email,
        f"New reply on ticket: {ticket.subject}",
        recipients,
        (
            f"{format_display_name(current_user)} replied to ticket {ticket.id}.\n\n"
            f"{comment.message}\n"
        ),
    )

    return {
        "message": "Comment added successfully.",
        "comment_id": comment.id,
        "comment": {
            "id": str(comment.id),
            "user_id": str(comment.user_id),
            "user_name": format_display_name(current_user),
            "user_role": current_user.role,
            "message": comment.message,
            "timestamp": comment.timestamp.isoformat(),
        },
    }


@tickets.get("/{ticket_id}/comments")
def get_comments(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    if (
        current_user.role != "admin"
        and current_user.user_id != ticket.assigned_to
        and current_user.user_id != ticket.created_by
    ):
        raise HTTPException(
            status_code=403, detail="You do not have access to this ticket"
        )

    comments = (
        db.query(Comment)
        .options(joinedload(Comment.user))
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.timestamp.asc())
        .all()
    )

    return {
        "ticket_id": ticket_id,
        "comments": [
            {
                "id": str(comment.id),
                "user_id": str(comment.user_id),
                "user_name": format_display_name(comment.user)
                if comment.user
                else None,
                "user_role": comment.user.role if comment.user else None,
                "message": comment.message,
                "timestamp": comment.timestamp.isoformat(),
            }
            for comment in comments
        ],
    }


@tickets.get("/{ticket_id}/history", response_model=List[TicketHistoryResponse])
def get_ticket_history(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    ensure_can_view_ticket(current_user, ticket)

    history = (
        db.query(TicketHistory)
        .options(joinedload(TicketHistory.user))
        .filter(TicketHistory.ticket_id == ticket_id)
        .order_by(TicketHistory.timestamp.desc())
        .all()
    )

    return [
        TicketHistoryResponse(
            id=entry.id,
            ticket_id=entry.ticket_id,
            user_id=entry.user_id,
            action=entry.action,
            timestamp=entry.timestamp,
            user_name=format_display_name(entry.user) if entry.user else None,
        )
        for entry in history
    ]
