import pytest
from pydantic import ValidationError
from schemas import CommentCreate

COMMENT = {
    "body": "This is some body text for a comment"
}

# CommentCreate
def test_valid_comment_create():
    comment = CommentCreate(body=COMMENT["body"])
    assert comment.body == COMMENT["body"]

def test_strip_whitespace():
    comment = CommentCreate(body="   This is some body text for a comment     ")
    assert comment.body == COMMENT["body"]
    
@pytest.mark.parametrize("body, is_exception_raised", [
    (" ", True), 
    ("", True), 
    ("a" * 1, False)
])
def test_body_length_boundaries(body, is_exception_raised):
    if is_exception_raised:
        with pytest.raises(ValidationError):
            CommentCreate(body=body)
    else:
        assert CommentCreate(body=body)