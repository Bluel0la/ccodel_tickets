import json

from tests.conftest import auth_headers, create_user, login


def test_ticket_attachment_upload_list_and_download(client, db):
    student = create_user(db, role="student")
    session = login(client, student.email)
    headers = auth_headers(session["access_token"])

    ticket_payload = {
        "subject": "Attachment test",
        "description": "Please see the attached PDF.",
        "category": "Technical Issue",
        "priority": "medium",
    }
    ticket_response = client.post(
        "/api/v1/tickets/",
        data={"ticket_data": json.dumps(ticket_payload)},
        files={
            "attachments": (
                "evidence.pdf",
                b"%PDF-1.4 test attachment content",
                "application/pdf",
            )
        },
        headers=headers,
    )
    assert ticket_response.status_code == 200, ticket_response.text
    ticket = ticket_response.json()
    assert ticket["attachment_count"] == 1

    listed = client.get(
        f"/api/v1/tickets/{ticket['id']}/attachments", headers=headers
    )
    assert listed.status_code == 200, listed.text
    attachments = listed.json()
    assert len(attachments) == 1
    assert attachments[0]["original_filename"] == "evidence.pdf"
    assert attachments[0]["file_size"] > 0
    assert attachments[0]["download_url"]

    download = client.get(attachments[0]["download_url"], headers=headers)
    assert download.status_code == 200
    assert download.content == b"%PDF-1.4 test attachment content"


def test_unsupported_attachment_type_is_rejected(client, db):
    student = create_user(db, role="student")
    session = login(client, student.email)
    headers = auth_headers(session["access_token"])

    ticket_payload = {
        "subject": "Bad file",
        "description": "Unsupported executable.",
        "category": "Technical Issue",
    }
    response = client.post(
        "/api/v1/tickets/",
        data={"ticket_data": json.dumps(ticket_payload)},
        files={
            "attachments": (
                "payload.exe",
                b"MZ test",
                "application/x-msdownload",
            )
        },
        headers=headers,
    )
    assert response.status_code == 400
