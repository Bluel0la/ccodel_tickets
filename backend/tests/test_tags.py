from tests.conftest import auth_headers, create_ticket, create_user, login


def test_admin_can_create_and_attach_tags(client, db):
    admin = create_user(db, role="admin")
    student = create_user(db, role="student")
    admin_session = login(client, admin.email)
    student_session = login(client, student.email)
    admin_headers = auth_headers(admin_session["access_token"])
    student_headers = auth_headers(student_session["access_token"])

    created = client.post(
        "/api/v1/tags",
        json={"name": "Urgent"},
        headers=admin_headers,
    )
    assert created.status_code == 201, created.text
    tag = created.json()

    ticket = create_ticket(client, student_headers)

    attached = client.post(
        f"/api/v1/tickets/{ticket['id']}/tags/{tag['id']}",
        headers=admin_headers,
    )
    assert attached.status_code == 200, attached.text

    detail = client.get(
        f"/api/v1/tickets/{ticket['id']}", headers=student_headers
    )
    assert detail.status_code == 200
    assert detail.json()["tags"][0]["name"] == "Urgent"

    detached = client.delete(
        f"/api/v1/tickets/{ticket['id']}/tags/{tag['id']}",
        headers=admin_headers,
    )
    assert detached.status_code == 200

    detail_after = client.get(
        f"/api/v1/tickets/{ticket['id']}", headers=student_headers
    )
    assert detail_after.json()["tags"] == []
