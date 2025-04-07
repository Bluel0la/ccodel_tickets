from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.v1.models.ticket import Ticket
from api.v1.models.user import User  # Assuming you have a User model
from api.utils.authentication import get_current_user  
from sqlalchemy.sql import func
from datetime import datetime, timedelta

analytics = APIRouter()


def check_admin(current_user: User):
    """Helper function to restrict access to admins."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )


@analytics.get("/analytics/average-resolution-time", tags=["Analytics"])
def get_average_resolution_time(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Calculate the average resolution time for resolved tickets."""
    check_admin(current_user)

    avg_time = (
        db.query(
            func.avg(
                func.extract("epoch", Ticket.date_resolved)
                - func.extract("epoch", Ticket.date_created)
            )
        )
        .filter(Ticket.status == "resolved", Ticket.date_resolved.isnot(None))
        .scalar()
    )

    return {"average_resolution_time_seconds": avg_time if avg_time else None}


@analytics.get("/analytics/tickets-by-category", tags=["Analytics"])
def get_tickets_by_category(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Count tickets grouped by category based on user role.

    - Admin: Sees ticket count for all categories.
    - Support: Sees ticket count only for assigned tickets.
    """

    if current_user.role == "admin":
        categories = (
            db.query(Ticket.category, func.count(Ticket.id))
            .group_by(Ticket.category)
            .all()
        )

    elif current_user.role == "support":
        categories = (
            db.query(Ticket.category, func.count(Ticket.id))
            .filter(Ticket.assigned_to == current_user.user_id)
            .group_by(Ticket.category)
            .all()
        )

    else:
        raise HTTPException(status_code=403, detail="Access denied.")

    return {"tickets_by_category": {category: count for category, count in categories}}


@analytics.get("/analytics/urgent-tickets", tags=["Analytics"])
def get_urgent_tickets_count(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get total number of urgent tickets (priority: high)."""
    check_admin(current_user)

    count = db.query(Ticket).filter(Ticket.priority == "high").count()

    return {"total_urgent_tickets": count}


# Support Staff Endpoints


@analytics.get("/analytics/tickets-summary", tags=["Analytics"])
def get_tickets_summary(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get ticket statistics based on user role.

    - Admin: Gets global ticket stats.
    - Support: Gets stats only for assigned tickets.
    """

    if current_user.role == "admin":
        return {
            "total_open_tickets": db.query(Ticket)
            .filter(Ticket.status == "open")
            .count(),
            "total_in_progress_tickets": db.query(Ticket)
            .filter(Ticket.status == "in_progress")
            .count(),
            "total_urgent_tickets": db.query(Ticket)
            .filter(Ticket.priority == "high")
            .count(),
        }

    elif current_user.role == "support":
        return {
            "assigned_open_tickets": db.query(Ticket)
            .filter(Ticket.status == "open", Ticket.assigned_to == current_user.user_id)
            .count(),
            "assigned_in_progress_tickets": db.query(Ticket)
            .filter(
                Ticket.status == "in_progress",
                Ticket.assigned_to == current_user.user_id,
            )
            .count(),
            "assigned_urgent_tickets": db.query(Ticket)
            .filter(
                Ticket.priority == "high", Ticket.assigned_to == current_user.user_id
            )
            .count(),
        }
        
    elif current_user.role == "student":
        return{
            "total_open_tickets": db.query(Ticket)
            .filter(Ticket.status == "open", Ticket.created_by == current_user.user_id)
            .count(),
            "total_in_progress_tickets": db.query(Ticket)
            .filter(
                Ticket.status == "in_progress",
                Ticket.created_by == current_user.user_id,
            )
            .count(),
            "total_resolved_tickets": db.query(Ticket)
            .filter(
                Ticket.status == "resolved", Ticket.created_by == current_user.user_id
            )
            .count(),
        }

    else:
        raise HTTPException(status_code=403, detail="Access denied.")


@analytics.get("/analytics/total-students", tags=["Analytics"])
def get_total_students(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get the total number of students (Admin Only)."""
    check_admin(current_user)

    total_students = db.query(User).filter(User.role == "student").count()

    return {"total_students": total_students}


@analytics.get("/analytics/active-support-staff", tags=["Analytics"])
def get_active_support_staff(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get a list of currently active support staff (logged in)."""

    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403, detail="Access denied. Admin or Support role required."
        )

    active_threshold = datetime.utcnow() - timedelta(minutes=10)  # Last 10 min
    active_staff = (
        db.query(User)
        .filter(User.role == "support", User.last_active >= active_threshold)
        .all()
    )

    return {
        "active_support_staff": [
            {"user_id": u.user_id, "username": u.first_name} for u in active_staff
        ]
    }
