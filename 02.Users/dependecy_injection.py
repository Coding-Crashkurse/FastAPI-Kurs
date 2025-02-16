import os
from typing import Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import field_validator
from sqlmodel import Field, Session, SQLModel, UniqueConstraint, create_engine

engine = create_engine("sqlite:///users.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def remove_db():
    os.remove("users.db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    try:
        yield
    finally:
        remove_db()


class UserBase(SQLModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    age: int


class UserCreate(UserBase):
    repeat_password: str

    @field_validator("repeat_password", mode="before")
    def repeat_password_must_match(cls, v, values):
        print(v)
        print(values)
        if v != values["password"]:
            raise HTTPException(
                status_code=400, detail="Repeat password does not match password."
            )
        return v


class UserTable(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"), UniqueConstraint("username"))
    id: Optional[int] = Field(default=None, primary_key=True)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(lifespan=lifespan)


@app.post("/register/", status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = UserTable.model_validate(user)
    session.add(db_user)
    session.commit()
    return {"id": db_user.id, "message": "User created successfully"}


@app.get("/users/")
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(UserTable).all()
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
