from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.core.dependencies import get_current_user, require_admin
from api.db.database import get_db
from api.v1.models.tag import Tag
from api.v1.models.user import User
from api.v1.schemas.tickets import TagCreate, TagResponse
from api.v1.services.tickets import get_ticket_or_404, record_history

tags = APIRouter(tags=["Tags"])


@tags.get("/tags", response_model=List[TagResponse])
def list_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Tag).order_by(Tag.name.asc()).all()


@tags.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = db.query(Tag).filter(Tag.name == tag_data.name.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    tag = Tag(name=tag_data.name.strip())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@tags.delete("/tags/{tag_id}")
def delete_tag(
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}


@tags.post("/tickets/{ticket_id}/tags/{tag_id}", response_model=TagResponse)
def attach_tag(
    ticket_id: UUID,
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    if current_user.role != "admin" and ticket.assigned_to != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag not in ticket.tags:
        ticket.tags.append(tag)
        record_history(db, ticket_id, current_user.user_id, f"Tag added: {tag.name}")
        db.commit()

    return tag


@tags.delete("/tickets/{ticket_id}/tags/{tag_id}")
def detach_tag(
    ticket_id: UUID,
    tag_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket_or_404(db, ticket_id)
    if current_user.role != "admin" and ticket.assigned_to != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag in ticket.tags:
        ticket.tags.remove(tag)
        record_history(
            db, ticket_id, current_user.user_id, f"Tag removed: {tag.name}"
        )
        db.commit()

    return {"message": "Tag removed"}
