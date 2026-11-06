from pydantic import BaseModel, ConfigDict, EmailStr, Field, FutureDatetime
from typing import List, Literal


TOPICS = ["Politics", "Health", "Sport", "Tech"]
VALID_TOPICS = Literal[TOPICS]

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
    topics: List[VALID_TOPICS] = Field(min_length=1)
    expires_at: FutureDatetime