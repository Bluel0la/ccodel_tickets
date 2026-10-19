from tests.conftest import (
    auth_headers,
    create_user,
    login,
    register_student,
)


def test_register_login_me_refresh_and_logout(client):
    email, password = register_student(client)

    session = login(client, email, password)
    assert session["user"]["email"] == email
    assert session["user"]["user_id"]
    assert session["access_token"]
    assert session["refresh_token"]

    headers = auth_headers(session["access_token"])
    me = client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["user_id"] == session["user"]["user_id"]

    refreshed = client.post(
        "/api/v1/auth/refresh-token",
        json={"refresh_token": session["refresh_token"]},
    )
    assert refreshed.status_code == 200, refreshed.text
    new_session = refreshed.json()
    assert new_session["access_token"] != session["access_token"]
    assert new_session["refresh_token"] != session["refresh_token"]

    reused = client.post(
        "/api/v1/auth/refresh-token",
        json={"refresh_token": session["refresh_token"]},
    )
    assert reused.status_code == 401

    logout = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": new_session["refresh_token"]},
        headers=auth_headers(new_session["access_token"]),
    )
    assert logout.status_code == 200, logout.text

    revoked_access = client.get(
        "/api/v1/auth/me",
        headers=auth_headers(new_session["access_token"]),
    )
    assert revoked_access.status_code == 401

    revoked_refresh = client.post(
        "/api/v1/auth/refresh-token",
        json={"refresh_token": new_session["refresh_token"]},
    )
    assert revoked_refresh.status_code == 401


def test_inactive_user_cannot_login(client, db):
    user = create_user(db, role="student", password="password123")
    user.is_active = False
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "password123"},
    )
    assert response.status_code == 403


def test_invalid_credentials(client):
    email, _ = register_student(client)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "wrong-password"},
    )
    assert response.status_code == 401
