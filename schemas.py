from pydantic import BaseModel, ConfigDict, EmailStr, Field, FutureDatetime
from typing import Literal
from datetime import datetime
from enum import Enum


TOPICS = ["Politics", "Health", "Sport", "Tech"]
VALID_TOPICS = Literal[tuple(TOPICS)] # tuple is needed so the docs pick up the list
POST_STATUSES = Literal["Live", "Expired"]
POST_REACTION = Literal["like", "dislike"]

# User
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

# Token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
# Post
class PostCreate(BaseModel):
    title: str = Field(max_length=30)
    body: str
    # Check against our list of topics and always require at least 1 topic
    topics: set[VALID_TOPICS] = Field(min_length=1)
    expires_at: FutureDatetime
    
class Topic(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class CommentsResponse(BaseModel):
    body: str
    user: str   
class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    topics: list[Topic]
    expires_at: datetime
    comments: list[CommentsResponse]
    # likes: int
    
    model_config = ConfigDict(from_attributes=True)

class PostQuery(BaseModel):
    # Both are optional parameters
    topic: VALID_TOPICS | None = None
    status: POST_STATUSES | None = None
    
class PostReaction(BaseModel):
    value: POST_REACTION