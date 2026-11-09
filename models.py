from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, func, Table, UniqueConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, column_property
from datetime import datetime

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, insert_default=func.now())
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

# Association table for the many-to-many relationship between posts and topics
post_topics = Table(
    "post_topics",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("topic_id", ForeignKey("topics.id"), primary_key=True)
)
    
# Association pattern from SQLAlchemy because we have an addition field "reaction"   
class UserPostReaction(Base):
    __tablename__ = "user_post_reactions"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    reaction: Mapped[str] = mapped_column(String, nullable=False)
    
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Derived columns
    likes = column_property(
        select(func.count(UserPostReaction.id))
        .where(UserPostReaction.post_id == id)
        .where(UserPostReaction.reaction == "like")
        .correlate_except(UserPostReaction)
        .scalar_subquery()
    )
    
    dislikes = column_property(
        select(func.count(UserPostReaction.id))
        .where(UserPostReaction.post_id == id)
        .where(UserPostReaction.reaction == "dislike")
        .correlate_except(UserPostReaction)
        .scalar_subquery()
    )
    
    reactions_count = column_property(
        select(func.count(UserPostReaction.id))
        .where(UserPostReaction.post_id == id)
        .correlate_except(UserPostReaction)
        .scalar_subquery()
    )
    
    # A post belongs to a user
    user: Mapped["User"] = relationship(back_populates="posts")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # has many
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    topics: Mapped[List["Topic"]] = relationship(secondary="post_topics", back_populates="posts")
    reactions: Mapped[List["UserPostReaction"]] = relationship()
    
    # def likes(self):
    #     count = 0
    #     for reaction in self.reactions:
    #         if reaction.reaction == "like":
    #             count += 1
    #     return count
    
class Topic(Base):
    __tablename__ = "topics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    
    # has many
    posts: Mapped[List["Post"]] = relationship(secondary="post_topics", back_populates="topics")
    
class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    
    # A comment belongs to a user and a post
    user: Mapped["User"] = relationship(back_populates="comments")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    post: Mapped["Post"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
