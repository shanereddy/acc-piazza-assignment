from fastapi import FastAPI

import models
from database import engine, SessionLocal
from routers import health, auth, post
from schemas import TOPICS


def create_app(db_engine=engine):
    models.Base.metadata.create_all(bind=db_engine)
    seed_db()
    
    app = FastAPI()
    
    app.include_router(health.router, prefix="")
    app.include_router(auth.router, prefix="/auth")
    app.include_router(post.router, prefix="/posts")

    return app

# Creates records if they do not exist
def seed_db():
    db = SessionLocal()
    
    try:
        # seed topics
        for topic_name in TOPICS:
            existing_topic = (
                db.query(models.Topic)
                .filter(models.Topic.name == topic_name)
                .first()
            )
            
            if existing_topic is None:
                db.add(models.Topic(name= topic_name))
                
        db.commit()
    finally:
        db.close()
    