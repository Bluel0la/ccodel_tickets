from tests.conftest import (
    auth_headers,
    create_user,
    login,
    register_student,
    unique_email,
)


def _login_user(client, db, role):
    user = create_user(db, role=role)
    session = login(client, user.email)
    return user, session


def test_user_management_permissions_and_password_change(client, db):
    admin, admin_session = _login_user(client, db, "admin")
    student, student_session = _login_user(client, db, "student")
    other_student = create_user(db, role="student")

    admin_headers = auth_headers(admin_session["access_token"])
    student_headers = auth_headers(student_session["access_token"])

    forbidden = client.get("/api/v1/users/", headers=student_headers)
    assert forbidden.status_code == 403

    listing = client.get("/api/v1/users/?role=student", headers=admin_headers)
    assert listing.status_code == 200, listing.text
    listed_ids = {str(item["user_id"]) for item in listing.json()}
    assert str(student.user_id) in listed_ids
    assert str(other_student.user_id) in listed_ids

    own = client.get(f"/api/v1/users/{student.user_id}", headers=student_headers)
    assert own.status_code == 200

    other = client.get(
        f"/api/v1/users/{other_student.user_id}", headers=student_headers
    )
    assert other.status_code == 403

    password_change = client.put(
        "/api/v1/users/change-password",
        json={
            "old_password": "password123",
            "new_password": "new-password-123",
        },
        headers=student_headers,
    )
    assert password_change.status_code == 200, password_change.text

    new_session = login(client, student.email, "new-password-123")
    assert new_session["access_token"]

    deactivate = client.delete(
        f"/api/v1/users/{student.user_id}", headers=admin_headers
    )
    assert deactivate.status_code == 200, deactivate.text

    inactive_login = client.post(
        "/api/v1/auth/login",
        json={"email": student.email, "password": "new-password-123"},
    )
    assert inactive_login.status_code == 403

    self_deactivate = client.delete(
        f"/api/v1/users/{admin.user_id}", headers=admin_headers
    )
    assert self_deactivate.status_code == 400


def test_admin_can_create_support_user(client, db):
    admin, admin_session = _login_user(client, db, "admin")
    admin_headers = auth_headers(admin_session["access_token"])
    email = unique_email("support")

    response = client.post(
        "/api/v1/users/",
        json={
            "matric_number": "STAFF-001",
            "firstname": "Support",
            "lastname": "Agent",
            "email": email,
            "password": "password123",
            "role": "support",
        },
        headers=admin_headers,
    )
    assert response.status_code == 201, response.text
    assert response.json()["role"] == "support"

    support_session = login(client, email)
    assert support_session["user"]["role"] == "support"
