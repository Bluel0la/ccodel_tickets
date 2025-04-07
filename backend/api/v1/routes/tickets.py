from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from api.db.database import get_db
from api.v1.models.ticket import Ticket
from api.v1.schemas.tickets import TicketCreate, TicketResponse, TicketUpdate, TicketAssign, AttachmentResponse, CommentCreate
from api.utils.authentication import get_current_user
from api.v1.models.user import User
from typing import List, Dict, Any, Optional
from datetime import datetime
from api.v1.models.attachement import Attachment
import shutil
from pathlib import Path
from api.db.database import SessionLocal
import uuid
from api.v1.models.comment import Comment
import json
tickets = APIRouter(prefix="/tickets", tags=["Tickets"])


# Add attachements
# Storage directory for uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Ensure directory exists


# Create a new ticket
@tickets.post("/", response_model=TicketResponse)
def create_ticket(
    ticket_data: str = Form(...),  # Receive as string from form-data
    attachments: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ Parse the JSON string into a dictionary
    try:
        ticket_data = json.loads(ticket_data)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format in ticket_data"
        )

    # Create the ticket
    ticket = Ticket(
        subject=ticket_data["subject"],
        description=ticket_data["description"],
        category=ticket_data["category"],
        priority="low",
        assigned_by=None if current_user.role == "student" else current_user.user_id,
        created_by=current_user.user_id,
        date_created=datetime.utcnow(),
        status="open",
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # ✅ Handle Attachments (if provided)
    if attachments:
        saved_attachments = []
        for file in attachments:
            file_path = UPLOAD_DIR / f"{ticket.id}_{file.filename}"
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            attachment = Attachment(
                ticket_id=ticket.id,
                file_path=str(file_path),
                uploaded_at=datetime.utcnow(),
            )
            db.add(attachment)
            saved_attachments.append(attachment)

        db.commit()
        for attachment in saved_attachments:
            db.refresh(attachment)

    return ticket


@tickets.get("/assigned", response_model=List[TicketResponse])
def get_assigned_tickets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != "support":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only support staff can view assigned tickets.",
        )

    tickets = db.query(Ticket).filter(Ticket.assigned_to == current_user.user_id).all()

    if not tickets:
        raise HTTPException(
            status_code=404, detail="No tickets have been assigned to you yet."
        )

    return tickets


@tickets.get("/all", response_model=List[TicketResponse])
def get_all_tickets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Access denied. Only admins can view all tickets."
        )

    tickets = db.query(Ticket).all()

    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets have been created yet.")

    return tickets


@tickets.get("/submitted", response_model=List[TicketResponse])
def get_user_submitted_tickets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    tickets = db.query(Ticket).filter(Ticket.created_by == current_user.user_id).all()

    if not tickets:
        raise HTTPException(
            status_code=404, detail="You have not submitted any tickets yet."
        )

    return tickets


# Get a specific ticket
@tickets.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Admin can access any ticket
    if current_user.role == "admin":
        return ticket

    # Support staff can access only assigned tickets
    if current_user.role == "support" and ticket.assigned_to == current_user.user_id:
        return ticket

    # Regular users can access only their submitted tickets
    if current_user.role not in ["admin", "support"] and ticket.assigned_by == current_user.user_id:
        return ticket

    # If none of the conditions are met, deny access
    raise HTTPException(status_code=403, detail="You do not have permission to access this ticket.")


# Update ticket details
@tickets.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Admin can update anything
    if current_user.role == "admin":
        for key, value in ticket_data.dict(exclude_unset=True).items():
            setattr(ticket, key, value)

    # Support staff can update priority, status (to closed), assigned_to, and category
    elif current_user.role == "support":
        if ticket.assigned_to == current_user.user_id:
            if ticket_data.priority:
                ticket.priority = ticket_data.priority
            if ticket_data.status == "closed":
                ticket.status = "closed"
                ticket.closed_by = current_user.user_id  # Auto-assign closed_by to the support staff
            if ticket_data.assigned_to:
                ticket.assigned_to = ticket_data.assigned_to
            if ticket_data.category:
                ticket.category = ticket_data.category
        else:
            raise HTTPException(status_code=403, detail="You can only update tickets assigned to you.")

    # Regular users can only update the description
    elif ticket.assigned_by == current_user.user_id:
        if ticket_data.description:
            ticket.description = ticket_data.description
        else:
            raise HTTPException(status_code=403, detail="You can only edit the description of your ticket.")

    # If none of the conditions match, deny access
    else:
        raise HTTPException(status_code=403, detail="You do not have permission to update this ticket.")

    db.commit()
    db.refresh(ticket)
    return ticket


# Assign a ticket to a support agent
@tickets.put("/{ticket_id}/assign", response_model=Dict[str, Any])
def assign_ticket(
    ticket_id: UUID,
    assign_data: TicketAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Get the current user
):
    # Ensure only admins can assign tickets
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can assign tickets.")

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Ensure the assigned user is a support staff
    assigned_user = (
        db.query(User).filter(User.user_id == assign_data.assigned_to).first()
    )
    if not assigned_user or assigned_user.role != "support":
        raise HTTPException(
            status_code=400, detail="Tickets can only be assigned to support staff."
        )

    ticket.assigned_to = assign_data.assigned_to
    db.commit()
    db.refresh(ticket)

    return {
        "message": f"Ticket successfully assigned to {assigned_user.first_name} {assigned_user.last_name} (Support Staff).",
        "ticket": TicketResponse.from_orm(ticket),  # ✅ Convert to Pydantic model
    }



@tickets.put("/{ticket_id}/cancel", response_model=TicketResponse)
def cancel_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Only allow the creator or an admin to cancel the ticket
    if (
        current_user.role not in ["admin", "support"]
        and ticket.created_by != current_user.user_id
    ):
        raise HTTPException(
            status_code=403, detail="You do not have permission to cancel this ticket"
        )

    if ticket.status in ["closed"]:
        raise HTTPException(
            status_code=400, detail="Ticket is already cancelled or closed"
        )

    ticket.status = "closed"
    ticket.closed_by = current_user.user_id
    ticket.date_closed = datetime.utcnow()  # Optional: mark when it was cancelled

    db.commit()
    db.refresh(ticket)
    return ticket


# View Attachments for tickets
@tickets.get("/{ticket_id}/attachments", response_model=List[AttachmentResponse])
def get_ticket_attachments(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Fetch ticket and attachments in one query
    ticket = (
        db.query(Ticket)
        .options(joinedload(Ticket.attachments))  # ✅ Preload attachments
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # ✅ Access control checks (Admins can always access)
    if current_user.role != "admin":
        if (
            current_user.role == "support"
            and ticket.assigned_to != current_user.user_id
        ):
            raise HTTPException(
                status_code=403, detail="Access denied: Not assigned to this ticket"
            )
        if current_user.role != "support" and ticket.created_by != current_user.user_id:
            raise HTTPException(
                status_code=403, detail="Access denied: You did not create this ticket"
            )

    # ✅ Return ticket attachments directly
    return ticket.attachments if ticket.attachments else []


# Chat Endpoints
@tickets.post("/{ticket_id}/comments", status_code=201)
def add_comment(
    ticket_id: uuid.UUID,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Allow assigned support staff or the student who created the ticket to add a comment."""

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")

    # Ensure only the assigned support staff or the ticket creator can comment
    if current_user.user_id not in [ticket.assigned_to, ticket.created_by]:
        raise HTTPException(
            status_code=403, detail="You do not have access to this ticket."
        )

    comment = Comment(
        id=uuid.uuid4(),
        ticket_id=ticket_id,
        user_id=current_user.user_id,
        message=comment_data.message,
        timestamp=datetime.utcnow(),
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {"message": "Comment added successfully.", "comment_id": comment.id}


@tickets.get("/{ticket_id}/comments")
def get_comments(
    ticket_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all comments for a ticket (visible to the assigned support staff and student)."""

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")

    # Ensure only the assigned support staff or the ticket creator can view comments
    if current_user.user_id not in [ticket.assigned_to, ticket.created_by]:
        raise HTTPException(
            status_code=403, detail="You do not have access to this ticket."
        )

    comments = (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.timestamp.asc())
        .all()
    )

    return {
        "ticket_id": ticket_id,
        "comments": [
            {
                "id": c.id,
                "user_id": c.user_id,
                "message": c.message,
                "timestamp": c.timestamp.isoformat(),
            }
            for c in comments
        ],
    }
