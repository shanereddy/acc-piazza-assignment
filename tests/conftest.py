import os

os.environ["JWT_SECRET"] = "test-only-secret-not-for-deployment-123456789"

import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application import create_app
from database import get_db

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
expires_at = (datetime.now() + timedelta(10))
POST = {"title": "New Title for Post", "body": "This is a body of a post.", "topics": ["Tech"], "expires_at": expires_at.isoformat()}
HEALTH_POST = {"title": "New Title for a Health Post", "body": "This is a body of a health post.", "topics": ["Health"], "expires_at": expires_at.isoformat()}
COMMENT = {"body": "This is a comment from a user"}

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

# 3 Tech posts
@pytest.fixture
def user_posts(client, auth_users):
    
    client.headers["Authorization"] = f"Bearer {auth_users["Olga"]["token"]}"
    auth_users["Olga"]["post_id"] = client.post("/posts", json=POST).json()["id"]
    
    client.headers["Authorization"] = f"Bearer {auth_users["Nick"]["token"]}"
    auth_users["Nick"]["post_id"] = client.post("/posts", json=POST).json()["id"]
    
    client.headers["Authorization"] = f"Bearer {auth_users["Mary"]["token"]}"
    auth_users["Mary"]["post_id"] = client.post("/posts", json=POST).json()["id"]
    
    return auth_users

# Nick and Olga like Mary’s post
@pytest.fixture
def post_likes(client, user_posts):
    mary_post_id = user_posts["Mary"]["post_id"]
    
    # Nick likes Mary's post
    client.headers["Authorization"] = f"Bearer {user_posts["Nick"]["token"]}"
    assert client.get(f"/posts/{mary_post_id}").json()["likes"] == 0
    response = client.put(f"/posts/{mary_post_id}/reaction", json={"value": "like"})
    assert response.status_code == 200
    
    # Olga likes Mary's post
    client.headers["Authorization"] = f"Bearer {user_posts["Olga"]["token"]}"
    response = client.put(f"/posts/{mary_post_id}/reaction", json={"value": "like"})
    assert response.status_code == 200
    
    return user_posts

# Nestor likes Nick’s post and dislikes Mary’s post
@pytest.fixture
def post_dislikes(client, post_likes):
    nicks_post_id = post_likes["Nick"]["post_id"]
    mary_post_id = post_likes["Mary"]["post_id"]
    
    # Nestor likes Nick's post and dislikes Mary's post
    client.headers["Authorization"] = f"Bearer {post_likes["Nestor"]["token"]}"
    response = client.put(f"/posts/{nicks_post_id}/reaction", json={"value": "like"})
    assert response.status_code == 200
    response = client.put(f"/posts/{mary_post_id}/reaction", json={"value": "dislike"})
    assert response.status_code == 200
    
    return post_likes

# Nick and Olga each add at least two comments to Mary’s post
@pytest.fixture
def post_comments(client, post_dislikes):
    mary_post_id = post_dislikes["Mary"]["post_id"]
    
    client.headers["Authorization"] = f"Bearer {post_dislikes["Nick"]["token"]}"
    response = client.post(f"/posts/{mary_post_id}/comments", json=COMMENT)
    assert response.status_code == 201
    response = client.post(f"/posts/{mary_post_id}/comments", json=COMMENT)
    assert response.status_code == 201
    
    client.headers["Authorization"] = f"Bearer {post_dislikes["Olga"]["token"]}"
    response = client.post(f"/posts/{mary_post_id}/comments", json=COMMENT)
    assert response.status_code == 201
    response = client.post(f"/posts/{mary_post_id}/comments", json=COMMENT)
    assert response.status_code == 201
    
    return post_dislikes

# Nestor creates a Health post
@pytest.fixture
def all_seeded_posts(client, post_comments):
    client.headers["Authorization"] = f"Bearer {post_comments["Nestor"]["token"]}"
    response = client.post("/posts", json=HEALTH_POST)
    assert response.status_code == 201
    post_comments["Nestor"]["health_post_id"] = response.json()["id"]
    return post_comments