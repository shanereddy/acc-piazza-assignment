from datetime import datetime, timezone, timedelta

expires_at = (datetime.now(timezone.utc) + timedelta(10)).isoformat()
POST = {"title": "New Title for Post", "body": "This is a body of a post.", "topics": ["Politics"], "expires_at": expires_at}

def test_route_unauthenticated(client):
    assert client.post("/posts", json=POST).status_code == 401
    
def test_route_authenticated(auth_client):
    create_post = auth_client.post("/posts", json=POST)
    print(create_post.json())
    assert create_post.status_code == 201

def test_create_and_retrieve(client):
    created = client.post("/posts", json=POST)
    assert created.status_code == 201
    body = created.json()
    assert body == {"id": body["id"]}
    assert isinstance(body["id"], int)