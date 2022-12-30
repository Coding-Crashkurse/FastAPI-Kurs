import uvicorn
from db_and_models.session import create_db_and_tables, drop_tables, get_session
from db_and_models.models import User, Post, Like, Follower, UserModel, PostModel, LikeModel, FollowerModel
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from fastapi import HTTPException

app = FastAPI()


def create_post(post: PostModel, db: Session):
    user = db.exec(select(User).where(User.id == post.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    post = Post.from_orm(post)
    db.add(post)
    db.commit()
    return {"success": f"Post mit {post.id} von {post.user_id} erstellt"}


def create_user(usermodel: UserModel, db: Session):
    existing_user = db.exec(select(User).where(User.email == usermodel.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    # Create the new user
    user = User.from_orm(usermodel)
    db.add(user)
    db.commit()
    return {"success": f"User mit {user.id} erstellt"}


# Create function to handle like request
def create_like(like: LikeModel, db: Session):
    # Check if user and post exist
    user = db.exec(select(User).where(User.id == like.user_id)).first()
    post = db.exec(select(Post).where(Post.id == like.post_id)).first()
    if not user or not post:
        raise HTTPException(status_code=404, detail="User or post not found")

    existing_like = db.exec(select(Like).where(Like.user_id == like.user_id).where(Like.post_id == like.post_id)).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="User has already liked this post")

    # Create like object and add it to the database
    like = Like(user_id=like.user_id, post_id=like.post_id)
    db.add(like)
    db.commit()
    return {"success": "Like added"}


def create_follower(follower: FollowerModel, db: Session):
    # Check if user and followed_user exist
    current_user = db.exec(select(User).where(User.id == follower.user_id)).first()
    followed_user = db.exec(select(User).where(User.id == follower.follower_id)).first()
    if not current_user or not followed_user:
        raise HTTPException(status_code=404, detail="User or followed user not found")

    already_following = db.exec(select(Follower).where(Follower.user_id == follower.user_id).where(Follower.follower_id == follower.follower_id)).first()
    if already_following:
        raise HTTPException(status_code=404, detail=f"User {follower.user_id} folgt {follower.follower_id} bereits")

    # Create follower object and add it to the database
    new_follower = Follower.from_orm(follower)
    db.add(new_follower)
    db.commit()
    return {"success": "Follow added"}


def get_following(db: Session):
    following = db.exec(select(Follower)).all()
    return following

@app.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session = Depends(get_session)):
    followers = db.exec(select(Follower).where(Follower.follower_id == user_id)).all()

    if not followers:
        raise HTTPException(status_code=404, detail="No followers found for this user")
    return followers


@app.post("/users")
def create_user_endpoint(user: UserModel, db: Session = Depends(get_session)):
    return create_user(user, db)


@app.post("/posts")
def create_post_endpoint(post: PostModel, db: Session = Depends(get_session)):
    return create_post(post, db)


@app.post("/likes")
def create_like_endpoint(like: LikeModel, db: Session = Depends(get_session)):
    return create_like(like, db)


@app.delete("/likes/{like_id}")
def delete_like(like_id: int, db: Session = Depends(get_session)):
    like = db.exec(select(Like).where(Like.id == like_id)).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return {"success": "Like removed"}

@app.post("/followers")
def create_follower_endpoint(follower: FollowerModel, db: Session = Depends(get_session)):
    return create_follower(follower, db)


@app.get("/following/")
def get_following_endpoint(db: Session = Depends(get_session)):
    return get_following(db)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#
# @app.on_event("shutdown")
# def on_shutdown():
#     drop_tables()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
