from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from api.core.dependencies import get_current_user
from api.db.database import get_db
from api.v1.models.history import TicketHistory
from api.v1.models.ticket import Ticket
from api.v1.models.user import User
from api.v1.services.tickets import format_display_name

analytics = APIRouter()


def check_admin(current_user: User) -> None:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only.",
        )


def _scoped_query(db: Session, current_user: User):
    query = db.query(Ticket)
    if current_user.role == "support":
        query = query.filter(Ticket.assigned_to == current_user.user_id)
    elif current_user.role not in {"admin", "student"}:
        raise HTTPException(status_code=403, detail="Access denied.")
    return query


@analytics.get("/analytics/average-resolution-time", tags=["Analytics"])
def get_average_resolution_time(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {"admin", "support"}:
        raise HTTPException(status_code=403, detail="Access denied.")

    query = db.query(
        func.avg(
            func.extract("epoch", Ticket.date_resolved)
            - func.extract("epoch", Ticket.date_created)
        )
    ).filter(Ticket.date_resolved.isnot(None))
    if current_user.role == "support":
        query = query.filter(Ticket.assigned_to == current_user.user_id)

    avg_time = query.scalar()
    return {
        "average_resolution_time_seconds": float(avg_time) if avg_time else None
    }


@analytics.get("/analytics/tickets-by-category", tags=["Analytics"])
def get_tickets_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = _scoped_query(db, current_user)
    categories = query.with_entities(
        Ticket.category, func.count(Ticket.id)
    ).group_by(Ticket.category).all()

    return {"tickets_by_category": {category: count for category, count in categories}}


@analytics.get("/analytics/urgent-tickets", tags=["Analytics"])
def get_urgent_tickets_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_admin(current_user)
    count = db.query(Ticket).filter(Ticket.priority == "high").count()
    return {"total_urgent_tickets": count}


@analytics.get("/analytics/tickets-summary", tags=["Analytics"])
def get_tickets_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        base = db.query(Ticket)
        return {
            "total_tickets": base.count(),
            "total_open_tickets": base.filter(Ticket.status == "open").count(),
            "total_in_progress_tickets": base.filter(
                Ticket.status == "in_progress"
            ).count(),
            "total_resolved_tickets": base.filter(
                Ticket.status == "resolved"
            ).count(),
            "total_closed_tickets": base.filter(Ticket.status == "closed").count(),
            "total_urgent_tickets": base.filter(Ticket.priority == "high").count(),
        }

    if current_user.role == "support":
        base = db.query(Ticket).filter(Ticket.assigned_to == current_user.user_id)
        return {
            "assigned_total_tickets": base.count(),
            "assigned_open_tickets": base.filter(Ticket.status == "open").count(),
            "assigned_in_progress_tickets": base.filter(
                Ticket.status == "in_progress"
            ).count(),
            "assigned_resolved_tickets": base.filter(
                Ticket.status == "resolved"
            ).count(),
            "assigned_closed_tickets": base.filter(
                Ticket.status == "closed"
            ).count(),
            "assigned_urgent_tickets": base.filter(
                Ticket.priority == "high"
            ).count(),
        }

    if current_user.role == "student":
        base = db.query(Ticket).filter(Ticket.created_by == current_user.user_id)
        return {
            "total_tickets": base.count(),
            "total_open_tickets": base.filter(Ticket.status == "open").count(),
            "total_in_progress_tickets": base.filter(
                Ticket.status == "in_progress"
            ).count(),
            "total_resolved_tickets": base.filter(
                Ticket.status == "resolved"
            ).count(),
            "total_closed_tickets": base.filter(Ticket.status == "closed").count(),
        }

    raise HTTPException(status_code=403, detail="Access denied.")


@analytics.get("/analytics/ticket-trends", tags=["Analytics"])
def get_ticket_trends(
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {"admin", "support", "student"}:
        raise HTTPException(status_code=403, detail="Access denied.")

    start = (datetime.utcnow().replace(day=1) - timedelta(days=31 * (months - 1)))
    query = db.query(
        func.date_trunc("month", Ticket.date_created).label("month"),
        Ticket.status,
        func.count(Ticket.id),
    ).filter(Ticket.date_created >= start)

    if current_user.role == "support":
        query = query.filter(Ticket.assigned_to == current_user.user_id)
    elif current_user.role == "student":
        query = query.filter(Ticket.created_by == current_user.user_id)

    rows = query.group_by("month", Ticket.status).order_by("month").all()

    buckets = {}
    for month, ticket_status, count in rows:
        key = month.strftime("%Y-%m")
        bucket = buckets.setdefault(
            key,
            {"month": key, "open": 0, "in_progress": 0, "resolved": 0, "closed": 0},
        )
        bucket[ticket_status] = count

    return {"ticket_trends": [buckets[key] for key in sorted(buckets)]}


@analytics.get("/analytics/total-students", tags=["Analytics"])
def get_total_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_admin(current_user)
    total_students = db.query(User).filter(User.role == "student").count()
    return {"total_students": total_students}


@analytics.get("/analytics/active-support-staff", tags=["Analytics"])
def get_active_support_staff(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {"admin", "support"}:
        raise HTTPException(
            status_code=403, detail="Access denied. Admin or Support role required."
        )

    active_threshold = datetime.utcnow() - timedelta(minutes=10)
    active_staff = (
        db.query(User)
        .filter(
            User.role == "support",
            User.is_active.is_(True),
            User.last_active >= active_threshold,
        )
        .all()
    )

    return {
        "active_support_staff": [
            {
                "user_id": staff.user_id,
                "name": format_display_name(staff),
                "last_active": staff.last_active,
            }
            for staff in active_staff
        ]
    }


@analytics.get("/analytics/recent-activity", tags=["Analytics"])
def get_recent_activity(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {"admin", "support"}:
        raise HTTPException(status_code=403, detail="Access denied.")

    query = (
        db.query(TicketHistory)
        .options(
            joinedload(TicketHistory.user),
            joinedload(TicketHistory.ticket),
        )
        .join(Ticket, Ticket.id == TicketHistory.ticket_id)
    )
    if current_user.role == "support":
        query = query.filter(Ticket.assigned_to == current_user.user_id)

    entries = query.order_by(TicketHistory.timestamp.desc()).limit(limit).all()
    return {
        "recent_activity": [
            {
                "id": entry.id,
                "ticket_id": entry.ticket_id,
                "ticket_subject": entry.ticket.subject if entry.ticket else None,
                "user_id": entry.user_id,
                "user_name": format_display_name(entry.user)
                if entry.user
                else None,
                "action": entry.action,
                "timestamp": entry.timestamp,
            }
            for entry in entries
        ]
    }
