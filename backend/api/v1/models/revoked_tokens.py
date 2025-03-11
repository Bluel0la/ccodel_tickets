from sqlalchemy import Column, String, DateTime
from datetime import datetime, timedelta
from api.db.database import Base

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    token = Column(String, primary_key=True, index=True)
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=1))
