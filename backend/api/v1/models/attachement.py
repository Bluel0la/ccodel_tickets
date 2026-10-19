from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship

from api.db.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ticket_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_path = Column(String, nullable=False)
    storage_public_id = Column(String, nullable=True, index=True)
    resource_type = Column(String, nullable=True)
    original_filename = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="attachments")