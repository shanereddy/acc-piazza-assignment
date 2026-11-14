import jwt
import pytest

from security import hash_password, verify_password, ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta, timezone

USER = {"username": "student", "email": "student@example.com", "password": "secret123"}

def test_password_hash():
    hashed = hash_password(USER["password"])
    assert hashed != USER["password"]
    assert verify_password(USER["password"], hashed)
    assert not verify_password("wrong", hashed)

def test_duplicate_registration(client):
    registered = client.post("/auth/register", json=USER)
    assert registered.status_code == 201
    assert set(registered.json()) == {"id", "username", "email"}
    duplicate_registered = client.post("/auth/register", json=USER)
    assert duplicate_registered.status_code == 409

def test_invalid_registration_data(client):
    response = client.post("/auth/register", json={**USER, "email": "s"})
    assert response.status_code == 422

def test_login_wrong_password(client):
    registered = client.post("/auth/register", json=USER)
    assert registered.status_code == 201
    login = client.post("/auth/login", json={**USER, "password": "abc"})
    assert login.status_code == 401
    
@pytest.mark.parametrize("kind", ["missing", "invalid", "expired", "no-expiry", "unknown-user", "bad-signature"])
def test_reject_token(client, kind):
    client.post("/auth/register", json=USER)
    payload = {"sub": USER["email"], "exp": datetime.now(timezone.utc) + timedelta(minutes=10)}
    if kind == "expired":
        payload["exp"] = datetime(2000, 1, 1, tzinfo=timezone.utc)
    if kind == "no-expiry":
        del payload["exp"]
    if kind == "unknown-user":
        payload["sub"] = "unknown@example.com"
    key = "other-test-signing-key-12345678901234567890" if kind == "bad-signature" else SECRET_KEY
    token = "invalid" if kind == "invalid" else jwt.encode(payload, key, algorithm=ALGORITHM)
    headers = {} if kind == "missing" else {"Authorization": f"Bearer {token}"}
    assert client.get("/posts", headers=headers).status_code == 401