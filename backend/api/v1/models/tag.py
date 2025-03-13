from sqlalchemy import Column, Integer, String, Table, ForeignKey, UUID
from sqlalchemy.orm import relationship
from api.db.database import Base
import uuid

# Association Table for Many-to-Many Relationship between Tickets and Tags
ticket_tags = Table(
    "ticket_tags",
    Base.metadata,
    Column("ticket_id", UUID(as_uuid=True), ForeignKey("tickets.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
)
class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, nullable=False)

    tickets = relationship("Ticket", secondary=ticket_tags, back_populates="tags")
