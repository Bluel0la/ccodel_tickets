from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TicketBase(BaseModel):
    subject: str
    description: str
    priority: str
    category: str


class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    priority: Optional[str] = "low"


class TicketUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[UUID] = None
    category: Optional[str] = None


class TicketResponse(TicketBase):
    id: UUID
    status: str
    created_by: UUID
    assigned_to: Optional[UUID] = None
    assigned_by: Optional[UUID] = None
    closed_by: Optional[UUID] = None
    created_by_name: Optional[str] = None
    assigned_to_name: Optional[str] = None
    closed_by_name: Optional[str] = None
    attachment_count: int = 0
    date_created: datetime
    date_resolved: Optional[datetime] = None
    date_closed: Optional[datetime] = None
    tags: List[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TicketAssign(BaseModel):
    assigned_to: UUID


class TicketHistoryBase(BaseModel):
    action: str


class TicketHistoryResponse(TicketHistoryBase):
    id: UUID
    timestamp: datetime
    user_id: UUID
    ticket_id: UUID
    user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AttachmentBase(BaseModel):
    file_path: str


class AttachmentCreate(AttachmentBase):
    ticket_id: UUID


class AttachmentResponse(BaseModel):
    id: UUID
    original_filename: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[int] = None
    resource_type: Optional[str] = None
    uploaded_at: datetime
    download_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    message: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: UUID
    user_id: UUID
    user_name: Optional[str] = None
    user_role: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
