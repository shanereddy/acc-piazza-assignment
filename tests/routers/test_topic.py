import pytest

def test_route_unauthenticated(client):
    response = client.get("/topics/Tech/most-active")
    assert response.status_code == 401

# TC20
def test_most_active_post_TC20(client, all_seeded_posts):
    mary_post_id = all_seeded_posts["Mary"]["post_id"]
    client.headers["Authorization"] = f"Bearer {all_seeded_posts["Olga"]["token"]}"
    
    response = client.get("/topics/Tech/most-active")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == mary_post_id