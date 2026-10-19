from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.v1.models.history import TicketHistory
from api.v1.models.ticket import Ticket
from api.v1.models.user import User


def get_ticket_or_404(db: Session, ticket_id: UUID) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


def can_view_ticket(user: User, ticket: Ticket) -> bool:
    if user.role == "admin":
        return True
    if user.role == "support":
        return ticket.assigned_to == user.user_id
    return ticket.created_by == user.user_id


def ensure_can_view_ticket(user: User, ticket: Ticket) -> None:
    if not can_view_ticket(user, ticket):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this ticket",
        )


def record_history(
    db: Session,
    ticket_id: UUID,
    user_id: UUID,
    action: str,
) -> TicketHistory:
    entry = TicketHistory(
        ticket_id=ticket_id,
        user_id=user_id,
        action=action,
        timestamp=datetime.utcnow(),
    )
    db.add(entry)
    return entry


def format_display_name(user: User) -> str:
    return f"{user.first_name} {user.last_name}".strip()
