import jwt
import pytest

from security import hash_password, verify_password, ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta, timezone
from conftest import USERS


USER = USERS["Olga"]

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
    
# TC01
@pytest.mark.parametrize("user", [USERS["Olga"], USERS["Nick"], USERS["Mary"], USERS["Nestor"]])
def test_register_successfully_TC01(client, user):
    response = client.post("/auth/register", json=user)
    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["username"] == user["username"]
    assert body["email"] == user["email"]
    
# TC02
@pytest.mark.parametrize("user", [USERS["Olga"], USERS["Nick"], USERS["Mary"], USERS["Nestor"]])
def test_login_and_receive_token_TC02(client, user):
    client.post("/auth/register", json=user)
    response = client.post("/auth/login", json=user)
    token = response.json()["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user["email"]
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()

# TC03
@pytest.mark.parametrize("user, expected_status_code", [(USERS["Olga"], 401), (USERS["Nick"], 200), (USERS["Mary"], 200), (USERS["Nestor"], 200)])
def test_user_without_token_TC03(client, user, expected_status_code):
    client.post("/auth/register", json=user)
    response = client.post("/auth/login", json=user)
    token = None if user["username"] == "Olga" else response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    assert client.get("/posts", ).status_code == expected_status_code