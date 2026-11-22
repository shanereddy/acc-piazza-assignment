from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Annotated

from datetime import datetime, timezone
from models import Post, Topic, User
import schemas
from database import get_db
from security import get_current_user
from clock import utc_now

router = APIRouter()

@router.get("/{topic}/most-active", response_model=list[schemas.PostResponse])
def get_post(topic: Annotated[str, schemas.ValidTopics], db: Session = Depends(get_db), current_user: User = Depends(get_current_user), now: datetime = Depends(utc_now)):
    post = (
        db.query(Post)
        .options(joinedload(Post.topics)) # all topics
        .filter(Post.topics.any(Topic.name == topic)) # filter the topic requested
        .filter(now < Post.expires_at) # only Live posts
        # highest reaction_count first
        # newest created_at
        # ascending order of post ids
        .order_by(desc(Post.reactions_count), desc(Post.created_at), Post.id)
        .limit(1) # We need a list back so limit to 1 result
    )
    
    if post is None:
        return []
    
    return post