def test_health_check(client):
    assert client.get("/health").status_code == 200