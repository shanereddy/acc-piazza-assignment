import pytest
from datetime import datetime, timezone, timedelta
from conftest import USERS

expires_at = (datetime.now() + timedelta(10))
POST = {"title": "New Title for Post", "body": "This is a body of a post.", "topics": ["Tech"], "expires_at": expires_at.isoformat()}
COMMENT = {"body": "This is a comment from a user"}

def test_route_unauthenticated(client):
    assert client.post("/posts", json=POST).status_code == 401
    
# TC04
def test_create_tech_post_TC04(client, auth_users):
    client.headers["Authorization"] = f"Bearer {auth_users["Olga"]["token"]}"
    response = client.post("/posts", json=POST)
    assert response.status_code == 201
    body = response.json()
    print(body)
    assert isinstance(body["id"], int)
    assert body["user_id"] == auth_users["Olga"]["user_id"]
    
# TC05
def test_create_tech_post_TC05(client, auth_users):
    client.headers["Authorization"] = f"Bearer {auth_users["Olga"]["token"]}"
    client.post("/posts", json=POST)
    
    client.headers["Authorization"] = f"Bearer {auth_users["Nick"]["token"]}"
    response = client.post("/posts", json=POST)
    
    assert response.status_code == 201
    body = response.json()
    print(body)
    assert isinstance(body["id"], int)
    assert body["user_id"] == auth_users["Nick"]["user_id"]
    
# TC06
def test_create_tech_post_TC06(client, auth_users):
    client.headers["Authorization"] = f"Bearer {auth_users["Olga"]["token"]}"
    client.post("/posts", json=POST)
    
    client.headers["Authorization"] = f"Bearer {auth_users["Nick"]["token"]}"
    client.post("/posts", json=POST)
    
    client.headers["Authorization"] = f"Bearer {auth_users["Mary"]["token"]}"
    response = client.post("/posts", json=POST)
    
    assert response.status_code == 201
    body = response.json()
    print(body)
    assert isinstance(body["id"], int)
    assert body["user_id"] == auth_users["Mary"]["user_id"]
    
# TC07
@pytest.mark.usefixtures("user_posts")
def test_get_posts_by_tech_topic_TC07(client):
    response = client.get("/posts?topic=Tech")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 3
    for post in posts:
        assert post["likes"] == 0
        assert post["dislikes"] == 0
        assert post["comments"] == []

# TC08
def test_likes_on_a_post_TC08(client, post_likes):
    mary_post_id = post_likes["Mary"]["post_id"]
    
    client.headers["Authorization"] = f"Bearer {post_likes["Nick"]["token"]}"
    assert client.get(f"/posts/{mary_post_id}").json()["likes"] == 2
    
# TC09
def test_likes_and_dislikes_on_posts_TC09(client, post_dislikes):
    nicks_post_id = post_dislikes["Nick"]["post_id"]
    mary_post_id = post_dislikes["Mary"]["post_id"]
    
    client.headers["Authorization"] = f"Bearer {post_dislikes["Nestor"]["token"]}"
    assert client.get(f"/posts/{nicks_post_id}").json()["likes"] == 1
    assert client.get(f"/posts/{mary_post_id}").json()["dislikes"] == 1

# TC10
def test_counts_of_posts_TC10(client, post_dislikes):
    nicks_post_id = post_dislikes["Nick"]["post_id"]
    mary_post_id = post_dislikes["Mary"]["post_id"]
    client.headers["Authorization"] = f"Bearer {post_dislikes["Nestor"]["token"]}"
    # Mary's posts
    response = client.get(f"/posts/{mary_post_id}").json()
    assert response["likes"] == 2
    assert response["dislikes"] == 1
    # Nick's post
    response = client.get(f"/posts/{nicks_post_id}").json()
    assert response["likes"] == 1
    
# TC11
def test_user_likes_own_post_TC11(client, post_dislikes):
    mary_post_id = post_dislikes["Mary"]["post_id"]
    client.headers["Authorization"] = f"Bearer {post_dislikes["Mary"]["token"]}"
    response = client.put(f"/posts/{mary_post_id}/reaction", json={"value": "like"})
    assert response.status_code == 403
    
    response = client.get(f"/posts/{mary_post_id}").json()
    assert response["likes"] == 2

# TC12
def test_users_add_comments_to_post_TC12(client, post_comments):
    mary_post_id = post_comments["Mary"]["post_id"]
    client.headers["Authorization"] = f"Bearer {post_comments["Mary"]["token"]}"
    
    response = client.get(f"/posts/{mary_post_id}").json()
    assert len(response["comments"]) == 4

# TC13
# def test_browsing_reactions_and_comments_TC13(client, auth_user_posts_with_likes):








# def test_route_authenticated(auth_client):
#     create_post = auth_client.post("/posts", json=POST)
#     print(create_post.json())
#     assert create_post.status_code == 201
    
  

# def test_create(auth_client, auth_user):
#     created = auth_client.post("/posts", json=POST)
#     assert created.status_code == 201
#     body = created.json()
#     assert isinstance(body["id"], int)
#     assert body["title"] == POST["title"]
#     assert body["body"] == POST["body"]
#     assert body["topics"][0]["name"] == POST["topics"][0]
#     assert datetime.fromisoformat(body["expires_at"]) == expires_at
#     assert body["likes"] == 0
#     assert body["dislikes"] == 0
#     assert body["comments"] == []
#     assert body["user_id"] == auth_user["id"]
    
# def test_create_incorrect_topic(auth_client):
#     created = auth_client.post("/posts", json={**POST, "topics": "fakeTopic"})
#     assert created.status_code == 201
    