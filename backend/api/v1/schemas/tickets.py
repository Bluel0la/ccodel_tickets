from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, List

class TicketBase(BaseModel):
    subject: str
    description: str
    priority: str  # "low", "medium", "high"
    category: str


class TicketCreate(BaseModel):
    subject: str
    description: str
    category: str


class TicketUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None  # "open", "in_progress", "resolved", "closed"
    assigned_to: Optional[UUID4] = None
    closed_by: Optional[UUID4] = None
    category: Optional[str] = None

class TicketResponse(TicketBase):
    id: UUID4
    status: str
    assigned_to: Optional[UUID4] = None
    assigned_by: Optional[UUID4]
    closed_by: Optional[UUID4] = None
    date_created: datetime
    date_resolved: Optional[datetime] = None
    date_closed: Optional[datetime] = None

    class Config:
        from_attributes = True

class TicketAssign(BaseModel):
    assigned_to: UUID4


class TicketHistoryBase(BaseModel):
    action: str

class TicketHistoryResponse(TicketHistoryBase):
    id: UUID4
    timestamp: datetime
    user_id: UUID4
    ticket_id: UUID4

    class Config:
        from_attributes = True

class AttachmentBase(BaseModel):
    file_path: str

class AttachmentCreate(AttachmentBase):
    ticket_id: UUID4

class AttachmentResponse(AttachmentBase):
    id: UUID4
    uploaded_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    message: str


class CommentCreate(BaseModel):
    message: str


class CommentResponse(CommentBase):
    id: UUID4
    timestamp: datetime

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass  # Only needs name

class TagResponse(TagBase):
    id: UUID4

    class Config:
        from_attributes = True

class TicketTagAssociation(BaseModel):
    ticket_id: UUID4
    tag_id: UUID4
