import os

os.environ["JWT_SECRET"] = "test-only-secret-not-for-deployment-123456789"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application import create_app
from database import get_db

# USER = {"username": "somesuer123", "email": "someuser@example.com", "password": "secret123"}
USERS =  {
    "Olga": 
    {"username": "Olga", "email": "olga@example.com", "password": "olgasecret123"},
    "Nick": 
    {"username": "Nick", "email": "nick@example.com", "password": "nicksecret123"},
    "Mary": 
    {"username": "Mary", "email": "mary@example.com", "password": "marysecret123"},
    "Nestor": 
    {"username": "Nestor", "email": "nestor@example.com", "password": "nestorsecret123"},
}

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
        
@pytest.fixture(params=[USERS["Olga"], USERS["Nick"], USERS["Mary"], USERS["Nestor"]])
def register_users(client, request):
    response = client.post("/auth/register", json=request.param)
    return response
        
@pytest.fixture
def auth_users(client):
    auth_users = {}
    
    for user in list(USERS.keys()):
        auth_users[user] = {}
        
        reg_response = client.post("/auth/register", json=USERS[user])
        auth_users[user]["user_id"] = reg_response.json()["id"]
        
        response = client.post("/auth/login", json=USERS[user])
        token = response.json()["access_token"]
        auth_users[user]["token"] = token
    
    return auth_users