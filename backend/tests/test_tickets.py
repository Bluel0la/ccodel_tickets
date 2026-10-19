import json

from tests.conftest import (
    auth_headers,
    create_ticket,
    create_user,
    login,
)


def _setup(client, db):
    admin = create_user(db, role="admin")
    support = create_user(db, role="support")
    student = create_user(db, role="student")
    other_student = create_user(db, role="student")

    admin_session = login(client, admin.email)
    support_session = login(client, support.email)
    student_session = login(client, student.email)
    other_session = login(client, other_student.email)

    return {
        "admin": admin,
        "support": support,
        "student": student,
        "other_student": other_student,
        "admin_headers": auth_headers(admin_session["access_token"]),
        "support_headers": auth_headers(support_session["access_token"]),
        "student_headers": auth_headers(student_session["access_token"]),
        "other_headers": auth_headers(other_session["access_token"]),
    }


def test_ticket_lifecycle_permissions_comments_and_history(client, db):
    data = _setup(client, db)

    ticket = create_ticket(client, data["student_headers"])
    assert ticket["priority"] == "high"
    assert ticket["created_by"] == str(data["student"].user_id)
    assert ticket["status"] == "open"

    submitted = client.get(
        "/api/v1/tickets/submitted", headers=data["student_headers"]
    )
    assert submitted.status_code == 200
    assert [item["id"] for item in submitted.json()] == [ticket["id"]]

    detail = client.get(
        f"/api/v1/tickets/{ticket['id']}", headers=data["student_headers"]
    )
    assert detail.status_code == 200, detail.text

    forbidden = client.get(
        f"/api/v1/tickets/{ticket['id']}", headers=data["other_headers"]
    )
    assert forbidden.status_code == 403

    all_tickets = client.get("/api/v1/tickets/all", headers=data["admin_headers"])
    assert all_tickets.status_code == 200
    assert any(item["id"] == ticket["id"] for item in all_tickets.json())

    support_forbidden = client.get(
        "/api/v1/tickets/all", headers=data["support_headers"]
    )
    assert support_forbidden.status_code == 403

    assigned = client.put(
        f"/api/v1/tickets/{ticket['id']}/assign",
        json={"assigned_to": str(data["support"].user_id)},
        headers=data["admin_headers"],
    )
    assert assigned.status_code == 200, assigned.text
    assert assigned.json()["ticket"]["assigned_to_name"] == "Test User"
    assert assigned.json()["ticket"]["status"] == "in_progress"

    assigned_list = client.get(
        "/api/v1/tickets/assigned", headers=data["support_headers"]
    )
    assert assigned_list.status_code == 200
    assert [item["id"] for item in assigned_list.json()] == [ticket["id"]]

    comment = client.post(
        f"/api/v1/tickets/{ticket['id']}/comments",
        json={"message": "We are looking into this."},
        headers=data["support_headers"],
    )
    assert comment.status_code == 201, comment.text
    assert comment.json()["comment"]["user_role"] == "support"

    comments = client.get(
        f"/api/v1/tickets/{ticket['id']}/comments",
        headers=data["student_headers"],
    )
    assert comments.status_code == 200
    assert comments.json()["comments"][0]["message"] == "We are looking into this."

    resolved = client.put(
        f"/api/v1/tickets/{ticket['id']}",
        json={"status": "resolved"},
        headers=data["support_headers"],
    )
    assert resolved.status_code == 200, resolved.text
    assert resolved.json()["status"] == "resolved"
    assert resolved.json()["date_resolved"] is not None

    history = client.get(
        f"/api/v1/tickets/{ticket['id']}/history",
        headers=data["student_headers"],
    )
    assert history.status_code == 200
    actions = [entry["action"] for entry in history.json()]
    assert "Ticket created" in actions
    assert any("Assigned to" in action for action in actions)
    assert "Comment added" in actions
    assert any("Status changed" in action for action in actions)

    student_priority_change = client.put(
        f"/api/v1/tickets/{ticket['id']}",
        json={"priority": "low"},
        headers=data["student_headers"],
    )
    assert student_priority_change.status_code == 403

    description_update = client.put(
        f"/api/v1/tickets/{ticket['id']}",
        json={"description": "Additional details from the student."},
        headers=data["student_headers"],
    )
    assert description_update.status_code == 200

    empty = client.get(
        "/api/v1/tickets/submitted", headers=data["other_headers"]
    )
    assert empty.status_code == 200
    assert empty.json() == []


def test_student_can_cancel_own_ticket(client, db):
    data = _setup(client, db)
    ticket = create_ticket(client, data["student_headers"])

    cancelled = client.put(
        f"/api/v1/tickets/{ticket['id']}/cancel",
        headers=data["student_headers"],
    )
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "closed"
    assert cancelled.json()["date_closed"] is not None

    other_cancel = create_ticket(client, data["student_headers"])
    forbidden = client.put(
        f"/api/v1/tickets/{other_cancel['id']}/cancel",
        headers=data["other_headers"],
    )
    assert forbidden.status_code == 403


def test_support_cannot_update_unassigned_ticket(client, db):
    data = _setup(client, db)
    ticket = create_ticket(client, data["student_headers"])

    response = client.put(
        f"/api/v1/tickets/{ticket['id']}",
        json={"status": "resolved"},
        headers=data["support_headers"],
    )
    assert response.status_code == 403
