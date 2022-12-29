from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class UserModel(SQLModel):
    username: str
    email: str
    password: str
    name: str

class User(UserModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    posts: list["Post"] = Relationship(back_populates="author")
    likes: list["Like"] = Relationship(back_populates="user")
    following: list["Follower"] = Relationship(back_populates="user")
    followers: list["Follower"] = Relationship(back_populates="followed_user")


class PostModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    content: str


class Post(PostModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)

    author: Optional[User] = Relationship(back_populates="posts")
    likes: list["Like"] = Relationship(back_populates="post")


class LikeModel(SQLModel):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    post_id: Optional[int] = Field(default=None, foreign_key="posts.id")

class Like(LikeModel, table=True):
    __tablename__ = "likes"

    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="likes")
    post: Optional[Post] = Relationship(back_populates="likes")


class FollowerModel(SQLModel):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    followed_user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class Follower(FollowerModel, table=True):
    __tablename__ = "followers"

    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="following")
    followed_user: Optional[User] = Relationship(back_populates="followers")
