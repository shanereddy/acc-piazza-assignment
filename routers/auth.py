from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from security import create_access_token, hash_password, verify_password

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=schemas.TokenResponse)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    # Find the active user by email.
    user = db.query(models.User).filter(models.User.email == user_login.email, models.User.active == True).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}