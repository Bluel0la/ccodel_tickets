from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from api.db.database import Base
import uuid

class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    action = Column(Text, nullable=False)  # e.g., "Status changed to resolved", "Assigned to User X"
    timestamp = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="history")
    user = relationship("User")
