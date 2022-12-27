import os
from typing import Optional
import uvicorn
from fastapi import Depends, FastAPI

from sqlmodel import Field, Session, SQLModel, create_engine

# Set up the database
engine = create_engine("sqlite:///users.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def remove_db():
    os.remove("users.db")


class UserBase(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    age: int


class UserCreate(UserBase):
    pass


class UserTable(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.post("/register/")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = UserTable.from_orm(user)
    session.add(db_user)
    session.commit()
    return {"id": db_user.id, "message": "User created successfully"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
def on_shutdown():
    remove_db()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
