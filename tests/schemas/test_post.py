import pytest

from datetime import datetime, timezone, timedelta
from pydantic import ValidationError

from schemas import PostCreate, PostQuery, PostReaction, PostResponse
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
    

@pytest.mark.parametrize("title, is_exception_raised", [
    (" ", True), 
    ("", True), 
    ("a" * 31, True), 
    ("a" * 1, False), 
    ("a" * 30, False)
])
def test_title_length_boundaries(title, is_exception_raised):
    if is_exception_raised:
        with pytest.raises(ValidationError):
            PostCreate(title=title, body=POST["body"], topics=POST["topics"], expires_at=POST["expires_at"])
    else:
        assert PostCreate(title=title, body=POST["body"], topics=POST["topics"], expires_at=POST["expires_at"])
        
@pytest.mark.parametrize("body, is_exception_raised", [
    (" ", True), 
    ("", True), 
    ("a" * 1, False)
])
def test_body_length_boundaries(body, is_exception_raised):
    if is_exception_raised:
        with pytest.raises(ValidationError):
            PostCreate(title=POST["title"], body=body, topics=POST["topics"], expires_at=POST["expires_at"])
    else:
        assert PostCreate(title=POST["title"], body=body, topics=POST["topics"], expires_at=POST["expires_at"])
    
@pytest.mark.parametrize("topics, is_exception_raised", [
    (["Politics", "Health", "Sport", "Tech"], False),
    (["Politics", "Health", "Sport", "TechAndSport"], True),
    ([""], True),
    (["NotATopic"], True)
])
def test_valid_topics_boundaries(topics, is_exception_raised):
    if is_exception_raised:
        with pytest.raises(ValidationError):
            PostCreate(title=POST["title"], body=POST["body"], topics=topics, expires_at=POST["expires_at"])
    else:
        assert PostCreate(title=POST["title"], body=POST["body"], topics=topics, expires_at=POST["expires_at"])
        
@pytest.mark.parametrize("expires_at, is_exception_raised", [
    (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(seconds=1), True), 
    (datetime.now(timezone.utc).replace(tzinfo=None), True), 
    (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=1), False) 
])
def test_expires_at_boundaries(expires_at, is_exception_raised):
    if is_exception_raised:
        with pytest.raises(ValidationError):
            PostCreate(title=POST["title"], body=POST["body"], topics=POST["topics"], expires_at=expires_at)
    else:
        assert PostCreate(title=POST["title"], body=POST["body"], topics=POST["topics"], expires_at=expires_at)

# PostQuery
@pytest.mark.parametrize("topic, status", [
    ("Health", "Live"),
    ("Sport", "Expired"),
    (None, "Expired"),
    ("Sport", None),
    (None, None)
])
def test_valid_post_query(topic, status):
    post_query = PostQuery(topic=topic, status=status)
    assert post_query.topic == topic
    assert post_query.status == status
    
@pytest.mark.parametrize("topic, status", [
    ("HealthAndSport", "Alive"),
    ("", ""),
    (None, "Expiring"),
    ("Technical", None)
])
def test_invalid_post_query(topic, status):
    with pytest.raises(ValidationError):
        PostQuery(topic=topic, status=status)
        
# PostReaction
@pytest.mark.parametrize("reaction", ["like", "dislike"])
def test_valid_post_reaction(reaction):
    post_reaction = PostReaction(value=reaction)
    assert post_reaction.value == reaction
    
@pytest.mark.parametrize("reaction", ["", None, "love"])
def test_invalid_post_reaction(reaction):
    with pytest.raises(ValidationError):
        PostReaction(value=reaction)
        
# PostResponse
@pytest.mark.parametrize("expires_at, expected_status", [
    (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(seconds=1), "Expired"), 
    (datetime.now(timezone.utc).replace(tzinfo=None), "Expired"), 
    (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=1), "Live") 
])
def test_status_computed_field(expires_at, expected_status):
    post_response = PostResponse(
        id=1, 
        title=POST["title"], 
        body=POST["body"], 
        topics=[{"name": POST["topics"][0]}],
        expires_at=expires_at,
        likes=0,
        dislikes=0,
        comments=[],
        user_id=3
    )
    assert post_response.status == expected_status