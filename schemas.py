from pydantic import BaseModel, ConfigDict, EmailStr, Field, FutureDatetime, computed_field, model_serializer
from datetime import datetime
from enum import StrEnum
from rules import is_post_live

class ValidTopics(StrEnum):
    Politics = "Politics"
    Health = "Health"
    Sport = "Sport"
    Tech = "Tech"
    
class PostStatus(StrEnum):
    Live = "Live"
    Expired = "Expired"
    
class PostReaction(StrEnum):
    like = "like"
    dislike = "dislike"

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
    title: str = Field(min_length=1, max_length=30)
    body: str = Field(min_length=1)
    # Check against our topics and always require at least 1 topic
    topics: set[ValidTopics] = Field(min_length=1)
    expires_at: FutureDatetime
    
    model_config = ConfigDict(str_strip_whitespace=True)
class Topic(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_serializer
    def topic_name_to_str(self) -> str:
        return self.name

class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    topics: list[Topic]
    expires_at: datetime
    likes: int
    dislikes: int
    comments: list[CommentResponse]
    user_id: int
    
    @computed_field
    @property
    def status(self) -> str:
        if is_post_live(datetime.now(), self.expires_at):
            return PostStatus.Live
        else:
            return PostStatus.Expired
    
    model_config = ConfigDict(from_attributes=True)

class PostQuery(BaseModel):
    # Both are optional parameters
    topic: ValidTopics | None = None
    status: PostStatus | None = None
    
class PostReaction(BaseModel):
    value: PostReaction
    
class CommentCreate(BaseModel):
    body: str = Field(min_length=1)
    model_config = ConfigDict(str_strip_whitespace=True)
    
class CommentResponse(BaseModel):
    id: int
    post_id: int
    body: str = Field(json_schema_extra={"strip_whitespace": True})
    user_id: int
    created_at: datetime