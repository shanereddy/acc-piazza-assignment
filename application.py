from fastapi import FastAPI

import models
from database import engine
from routers import health
# from routers import auth


def create_app(db_engine=engine):
    # models.Base.metadata.create_all(bind=db_engine)
    app = FastAPI()
    app.include_router(health.router, prefix="")
    # app.include_router(auth.router, prefix="/auth")

    return app