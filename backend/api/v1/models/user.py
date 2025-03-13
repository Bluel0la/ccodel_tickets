from sqlalchemy import Column, String, Enum, UUID, Boolean
from sqlalchemy.orm import relationship
import uuid

from api.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    matric_number = Column(String(255), unique=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    role = Column(Enum("admin", "support", "student", name="role_enum"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)  # ✅ Added is_active column

    tickets_assigned = relationship("Ticket", back_populates="assigned_to_user", foreign_keys="Ticket.assigned_to")
    tickets_created = relationship("Ticket", back_populates="assigned_by_user", foreign_keys="Ticket.assigned_by")
    tickets_closed = relationship("Ticket", back_populates="closed_by_user", foreign_keys="Ticket.closed_by")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
