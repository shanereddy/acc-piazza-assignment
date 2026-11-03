import datetime as dt
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    active = mapped_column(Boolean, nullable=False, default=True)
    
# class Post(Base):
#     __tablename__ = "posts"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(30), nullable=False)
#     body = Column(Text, nullable=False)
#     status = Column(String(30), nullable=False, default="Live") # New posts are created as Live
#     expires_at = Column(DateTime, nullable=False)
#     created_at = Column(DateTime, nullable=False, default=dt.datetime.now())