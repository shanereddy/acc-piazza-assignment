import pytest

from pydantic import ValidationError

from schemas import UserCreate, UserLogin

USER = {"username": "shane2807", "email": "shane@example.com", "password": "sample_password"}

# UserCreate
def test_valid_email_user_create():
    user = UserCreate(username=USER["username"], email=USER["email"], password=USER["password"])
    assert user.email == USER["email"]

def test_invalid_email_user_create():
    with pytest.raises(ValidationError):
        UserCreate(username=USER["username"], email="shaneatexample.com", password=USER["password"])

def test_no_username():
    with pytest.raises(ValidationError):
        UserCreate(email=USER["email"], password=USER["password"])

@pytest.mark.parametrize("username", [("ab"), ("a" * 51)])
def test_username_length_boundary_failure(username):
    with pytest.raises(ValidationError):
        UserCreate(username=username, email=USER["email"], password=USER["password"])
    
@pytest.mark.parametrize("username", [("a" * 3), ("a" * 50)])
def test_username_length_boundary_success(username):
    user = UserCreate(username=username, email=USER["email"], password=USER["password"])
    assert user.username == username

def test_invalid_short_password():
    with pytest.raises(ValidationError):
        UserCreate(username=USER["username"], email=USER["email"], password="b" * 5)

# UserLogin
def test_valid_email_user_login():
    user = UserLogin(email=USER["email"], password=USER["password"])
    assert user.email == USER["email"]

def test_invalid_email_user_login():
    with pytest.raises(ValidationError):
        UserLogin(email="shaneatexample.com", password=USER["password"])
