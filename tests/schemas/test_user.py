import pytest

from pydantic import ValidationError

from schemas import UserCreate, UserLogin

USER = {"email": "shane@example.com", "password": "sample_password"}

# UserCreate
def test_valid_email_user_create():
    user = UserCreate(email=USER["email"], password=USER["password"])
    assert user.email == USER["email"]
    assert user.active == True

def test_invalid_email_user_create():
    with pytest.raises(ValidationError):
        UserCreate(email="shaneatexample.com", password=USER["password"])

def test_invalid_password():
    with pytest.raises(ValidationError):
        UserCreate(email=USER["email"], password="short")

# UserLogin
def test_valid_email_user_login():
    user = UserLogin(email=USER["email"], password=USER["password"])
    assert user.email == USER["email"]

def test_invalid_email_user_login():
    with pytest.raises(ValidationError):
        UserLogin(email="shaneatexample.com", password=USER["password"])
