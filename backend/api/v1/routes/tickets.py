from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from api.db.database import get_db
from api.v1.models.ticket import Ticket
from api.v1.schemas.tickets import TicketCreate, TicketResponse, TicketUpdate, TicketAssign, AttachmentResponse
from api.utils.authentication import get_current_user
from api.v1.models.user import User
from typing import List, Dict, Any
from datetime import datetime
from api.v1.models.attachement import Attachment
import shutil
import os
from pathlib import Path
from api.db.database import SessionLocal
from datetime import timedelta
tickets = APIRouter(prefix="/tickets", tags=["Tickets"])


# Create a new ticket
@tickets.post("/", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ensure students cannot set priority or assigned_by
    ticket = Ticket(
        subject=ticket_data.subject,
        description=ticket_data.description,
        category=ticket_data.category,
        priority="low",  # Default priority is "low"
        assigned_by=(
            None if current_user.role == "student" else current_user.user_id
        ),  # Blank for students
        created_by=current_user.user_id,
        date_created=datetime.utcnow(),
        status="open",
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
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
    tickets = db.query(Ticket).filter(Ticket.assigned_by == current_user.user_id).all()

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
        "ticket": ticket,
    }


# Close a ticket
@tickets.put("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Only allow admin or the assigned support staff to close the ticket
    if current_user.role != "admin" and ticket.assigned_to != current_user.user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to close this ticket")

    ticket.status = "closed"
    ticket.closed_by = current_user.user_id
    ticket.date_closed = datetime.utcnow()
    
    db.commit()
    db.refresh(ticket)
    return ticket

# Delete a ticket (Admin only)
@tickets.put("/{ticket_id}/cancel", response_model=TicketResponse)
def cancel_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Only the ticket creator or an admin can cancel the ticket
    if current_user.role != "admin" and ticket.assigned_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to cancel this ticket")

    ticket.status = "cancelled"

    db.commit()
    db.refresh(ticket)
    return ticket

# Add attachements
# Storage directory for uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Ensure directory exists


@tickets.post("/{ticket_id}/attachments", response_model=AttachmentResponse)
def add_attachment(
    ticket_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Authorization: Only Admin, assigned support staff, or ticket creator can upload
    if current_user.role != "admin" and current_user.user_id not in [
        ticket.assigned_by,
        ticket.assigned_to,
    ]:
        raise HTTPException(
            status_code=403, detail="Unauthorized to upload attachments"
        )

    # Save file locally
    file_path = UPLOAD_DIR / f"{ticket_id}_{file.filename}"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save to DB
    attachment = Attachment(
        ticket_id=ticket_id, file_path=str(file_path), uploaded_at=datetime.utcnow()
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


# ✅ Background Task to Delete Old Attachments
def cleanup_old_attachments():
    db: Session = SessionLocal()
    try:
        expiry_time = datetime.utcnow() - timedelta(
            days=7
        )  # Delete files older than 7 days
        old_attachments = (
            db.query(Attachment).filter(Attachment.uploaded_at < expiry_time).all()
        )

        for attachment in old_attachments:
            file_path = Path(attachment.file_path)
            if file_path.exists():
                os.remove(file_path)  # Delete the file

            db.delete(attachment)  # Remove from database

        db.commit()
    finally:
        db.close()


# View Attachments for tickets
@tickets.get("/{ticket_id}/attachments", response_model=List[AttachmentResponse])
def get_ticket_attachments(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Fetch the ticket and its attachments in one query
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Access control logic
    if current_user.role == "admin":
        pass  # Admins can access all attachments
    elif current_user.role == "support":
        if ticket.assigned_to != current_user.user_id:
            raise HTTPException(
                status_code=403, detail="Access denied: Not assigned to this ticket"
            )
    else:  # Regular users
        if ticket.assigned_by != current_user.user_id:
            raise HTTPException(
                status_code=403, detail="Access denied: You did not create this ticket"
            )

    # Fetch attachments
    attachments = db.query(Attachment).filter(Attachment.ticket_id == ticket_id).all()

    if not attachments:
        raise HTTPException(
            status_code=404, detail="No attachments found for this ticket"
        )

    return attachments
