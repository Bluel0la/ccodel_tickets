import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func

from api.core.config import get_settings
from api.db.database import SessionLocal
from api.utils.authentication import hash_password
from api.v1.models.user import User


def seed_admin() -> None:
    settings = get_settings()
    if not settings.admin_email or not settings.admin_password:
        raise SystemExit(
            "ADMIN_EMAIL and ADMIN_PASSWORD must be set to seed an admin"
        )

    db = SessionLocal()
    try:
        email = settings.admin_email.lower()
        existing = db.query(User).filter(func.lower(User.email) == email).first()
        if existing:
            print(f"Admin already exists: {email}")
            return

        user = User(
            email=email,
            password=hash_password(settings.admin_password),
            first_name=settings.admin_first_name,
            last_name=settings.admin_last_name,
            matric_number=settings.admin_matric_number or None,
            role="admin",
            is_active=True,
        )
        db.add(user)
        db.commit()
        print(f"Created admin user: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
