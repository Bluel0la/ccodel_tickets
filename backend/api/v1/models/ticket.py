from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from api.db.database import Base
import uuid

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum("low", "medium", "high", name="priority_enum"), nullable=False)
    status = Column(Enum("open", "in_progress", "resolved", "closed", name="status_enum"), default="open", nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    closed_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    category = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_resolved = Column(DateTime, nullable=True)
    date_closed = Column(DateTime, nullable=True)

    assigned_to_user = relationship("User", foreign_keys=[assigned_to], backref="assigned_tickets")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by], backref="created_tickets")
    closed_by_user = relationship("User", foreign_keys=[closed_by], backref="closed_tickets")

    attachments = relationship("Attachment", back_populates="ticket", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")
    history = relationship("TicketHistory", back_populates="ticket", order_by="TicketHistory.timestamp.desc()", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="ticket_tags", back_populates="tickets")