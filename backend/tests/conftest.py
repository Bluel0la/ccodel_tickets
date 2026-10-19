import os
import tempfile
import uuid

import pytest

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    pytest.skip(
        "TEST_DATABASE_URL is required; tests are never run against the application database",
        allow_module_level=True,
    )

from sqlalchemy.engine import make_url

test_database_name = make_url(TEST_DATABASE_URL).database or ""
if "test" not in test_database_name.lower():
    pytest.exit(
        "TEST_DATABASE_URL must point to a database whose name contains 'test'",
        returncode=2,
    )

os.environ["DB_URL"] = TEST_DATABASE_URL
os.environ["SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"
os.environ["MAIL_ENABLED"] = "False"
os.environ["STORAGE_BACKEND"] = "local"
os.environ["UPLOAD_DIR"] = tempfile.mkdtemp(prefix="ccodel-test-uploads-")
os.environ["FRONTEND_URLS"] = "http://testserver"

from fastapi.testclient import TestClient

from api.core.config import get_settings

get_settings.cache_clear()

from api.db.database import Base, SessionLocal, db_engine
from api.utils.authentication import hash_password
from api.v1.models.user import User
from main import app  # noqa: E402


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db(client):
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def unique_email(prefix: str = "user") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}@example.com"


def create_user(
    db,
    role: str = "student",
    email: str | None = None,
    password: str = "password123",
    first_name: str = "Test",
    last_name: str = "User",
):
    email = email or unique_email(role)
    user = User(
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        matric_number=f"MAT-{uuid.uuid4().hex[:8]}",
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(client, email: str, password: str = "password123") -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def register_student(client, email: str | None = None, password: str = "password123"):
    email = email or unique_email("student")
    response = client.post(
        "/api/v1/auth/register",
        json={
            "matric_number": f"MAT-{uuid.uuid4().hex[:8]}",
            "firstname": "Test",
            "lastname": "Student",
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 201, response.text
    return email, password


def create_ticket(client, token, **overrides):
    payload = {
        "subject": "Cannot access course materials",
        "description": "The course materials page returns an error.",
        "category": "Technical Issue",
        "priority": "high",
    }
    payload.update(overrides)
    headers = token if isinstance(token, dict) else auth_headers(token)
    response = client.post(
        "/api/v1/tickets/",
        data={"ticket_data": __import__("json").dumps(payload)},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()
