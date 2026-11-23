import pytest

from datetime import timedelta
from pydantic import ValidationError

from schemas import ValidTopics, PostCreate
from clock import utc_now

POST = {
    "title": "This is a Test Title", 
    "body": "This is some body text for a post", 
    "topics": ["Health"], 
    "expires_at": utc_now() + timedelta(minutes=10)
}

# PostCreate
def test_valid_post_create():
    post = PostCreate(title=POST["title"], body=POST["body"], topics=POST["topics"], expires_at=POST["expires_at"])
    assert post.title == POST["title"]
    assert post.body == POST["body"]
    assert {t.value for t in post.topics} == set(POST["topics"])
    assert post.expires_at == POST["expires_at"]

def test_strip_whitespace():
    post = PostCreate(title=f"  {POST["title"]}   ", body=f"  {POST["body"]}  ", topics=POST["topics"], expires_at=POST["expires_at"])
    assert post.title == POST["title"]
    assert post.body == POST["body"]
    
    
    
# def test_invalid_email_user_create():
#     with pytest.raises(ValidationError):
#         UserCreate(username=USER["username"], email="shaneatexample.com", password=USER["password"])

# def test_no_username():
#     with pytest.raises(ValidationError):
#         UserCreate(email=USER["email"], password=USER["password"])

# @pytest.mark.parametrize("username", [("ab"), ("a" * 51)])
# def test_username_length_boundary_failure(username):
#     with pytest.raises(ValidationError):
#         UserCreate(username=username, email=USER["email"], password=USER["password"])
    
# @pytest.mark.parametrize("username", [("a" * 3), ("a" * 50)])
# def test_username_length_boundary_success(username):
#     user = UserCreate(username=username, email=USER["email"], password=USER["password"])
#     assert user.username == username

# def test_invalid_short_password():
#     with pytest.raises(ValidationError):
#         UserCreate(username=USER["username"], email=USER["email"], password="b" * 5)

# # UserLogin
# def test_valid_email_user_login():
#     user = UserLogin(email=USER["email"], password=USER["password"])
#     assert user.email == USER["email"]

# def test_invalid_email_user_login():
#     with pytest.raises(ValidationError):
#         UserLogin(email="shaneatexample.com", password=USER["password"])
