from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.PostResponse, status_code=201)
def create(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Create new post
    new_post = models.Post(
        title=post.title,
        body=post.body,
        expires_at=post.expires_at
    )
    
    # associate the user
    new_post.user = current_user
    
    for topic in post.topics:
        existing_topic = (db.query(models.Topic)
            .filter(models.Topic.name == topic)
            .first()
        )
        
        if existing_topic is None:
            raise HTTPException(status_code=409, detail="Existing topic not found")
        
        new_post.topics.append(existing_topic)

    db.add(new_post)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Post not created")
    db.refresh(new_post)
    return new_post