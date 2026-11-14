import os

os.environ["JWT_SECRET"] = "test-only-secret-not-for-deployment-123456789"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application import create_app
from database import get_db

USER = {"username": "somesuer123", "email": "someuser@example.com", "password": "secret123"}

@pytest.fixture
def client(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'piazza-test.db'}",
        connect_args={"check_same_thread": False},
    )
    sessions = sessionmaker(bind=engine)
    app = create_app(engine)

    def override_db():
        with sessions() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
        
@pytest.fixture
def auth_client(client):
    client.post("/auth/register", json=USER)
    response = client.post("/auth/login", json=USER)
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client