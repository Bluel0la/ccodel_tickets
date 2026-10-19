from tests.conftest import auth_headers, create_ticket, create_user, login


def _setup(client, db):
    admin = create_user(db, role="admin")
    support = create_user(db, role="support")
    student = create_user(db, role="student")

    admin_session = login(client, admin.email)
    support_session = login(client, support.email)
    student_session = login(client, student.email)

    admin_headers = auth_headers(admin_session["access_token"])
    support_headers = auth_headers(support_session["access_token"])
    student_headers = auth_headers(student_session["access_token"])

    client.get("/api/v1/auth/me", headers=support_headers)

    ticket = create_ticket(client, student_headers, priority="high")
    client.put(
        f"/api/v1/tickets/{ticket['id']}/assign",
        json={"assigned_to": str(support.user_id)},
        headers=admin_headers,
    )
    client.put(
        f"/api/v1/tickets/{ticket['id']}",
        json={"status": "resolved"},
        headers=support_headers,
    )

    return {
        "admin_headers": admin_headers,
        "support_headers": support_headers,
        "student_headers": student_headers,
    }


def test_admin_analytics(client, db):
    data = _setup(client, db)
    headers = data["admin_headers"]

    summary = client.get("/api/v1/analytics/tickets-summary", headers=headers)
    assert summary.status_code == 200, summary.text
    payload = summary.json()
    assert payload["total_tickets"] == 1
    assert payload["total_resolved_tickets"] == 1
    assert payload["total_urgent_tickets"] == 1

    categories = client.get(
        "/api/v1/analytics/tickets-by-category", headers=headers
    )
    assert categories.status_code == 200
    assert categories.json()["tickets_by_category"]["Technical Issue"] == 1

    trends = client.get("/api/v1/analytics/ticket-trends", headers=headers)
    assert trends.status_code == 200, trends.text
    assert len(trends.json()["ticket_trends"]) == 1
    assert trends.json()["ticket_trends"][0]["resolved"] == 1

    resolution = client.get(
        "/api/v1/analytics/average-resolution-time", headers=headers
    )
    assert resolution.status_code == 200
    assert resolution.json()["average_resolution_time_seconds"] is not None

    students = client.get("/api/v1/analytics/total-students", headers=headers)
    assert students.status_code == 200
    assert students.json()["total_students"] == 1

    active = client.get(
        "/api/v1/analytics/active-support-staff", headers=headers
    )
    assert active.status_code == 200
    assert len(active.json()["active_support_staff"]) == 1

    activity = client.get("/api/v1/analytics/recent-activity", headers=headers)
    assert activity.status_code == 200
    assert len(activity.json()["recent_activity"]) >= 1


def test_support_and_student_analytics_are_scoped(client, db):
    data = _setup(client, db)

    support_summary = client.get(
        "/api/v1/analytics/tickets-summary",
        headers=data["support_headers"],
    )
    assert support_summary.status_code == 200
    assert support_summary.json()["assigned_total_tickets"] == 1
    assert support_summary.json()["assigned_resolved_tickets"] == 1

    student_summary = client.get(
        "/api/v1/analytics/tickets-summary",
        headers=data["student_headers"],
    )
    assert student_summary.status_code == 200
    assert student_summary.json()["total_tickets"] == 1

    student_cannot_view_students = client.get(
        "/api/v1/analytics/total-students",
        headers=data["student_headers"],
    )
    assert student_cannot_view_students.status_code == 403
