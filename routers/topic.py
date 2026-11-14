from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Annotated, Literal
from fastapi import Query

from datetime import datetime, timezone
import models
import schemas
from database import get_db
from security import get_current_user

router = APIRouter()

@router.get("/{topic}/most-active", response_model=list[schemas.PostResponse])
def get_post(topic: Annotated[str, schemas.ValidTopics], db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = (
        db.query(models.Post)
        .options(joinedload(models.Post.topics)) # all topics
        .filter(models.Post.topics.any(models.Topic.name == topic)) # filter the topic requested
        .filter(datetime.now(timezone.utc) < models.Post.expires_at) # only Live posts
        # highest reaction_count first
        # newest created_at
        # ascending order of post ids
        .order_by(desc(models.Post.reactions_count), desc(models.Post.created_at), models.Post.id)
        .limit(1) # We need a list back so limit to 1 result
    )
    
    if post is None:
        return []
    
    return post