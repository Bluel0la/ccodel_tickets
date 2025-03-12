from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from api.v1.models.refresh_tokens import RefreshToken
from api.v1.models.revoked_tokens import RevokedToken
from api.db.database import SessionLocal

def cleanup_expired_tokens():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        # Delete expired revoked tokens
        db.query(RevokedToken).filter(RevokedToken.expires_at < now).delete()
        # Delete expired refresh tokens
        db.query(RefreshToken).filter(RefreshToken.expires_at < now).delete()
        db.commit()
    finally:
        db.close()
