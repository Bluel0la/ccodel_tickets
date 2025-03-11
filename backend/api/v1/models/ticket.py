from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from api.db.database import Base
import uuid

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    description = Column(Text, nullable=False)
    priority = Column(Enum("low", "medium", "high", name="priority_enum"), nullable=False)
    status = Column(Enum("open", "in_progress", "resolved", "closed", name="status_enum"), default="open", nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_resolved = Column(DateTime, nullable=True)
    date_closed = Column(DateTime, nullable=True)
    closed_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    category = Column(String, nullable=False)

    assigned_to_user = relationship("User", foreign_keys=[assigned_to])
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    closed_by_user = relationship("User", foreign_keys=[closed_by])

    attachments = relationship("Attachment", back_populates="ticket")
    comments = relationship("Comment", back_populates="ticket")
    history = relationship("TicketHistory", back_populates="ticket", order_by="TicketHistory.timestamp.desc()")
    tags = relationship("Tag", secondary="ticket_tags", back_populates="tickets")
