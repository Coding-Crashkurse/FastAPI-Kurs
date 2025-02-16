import os
from typing import Optional
from contextlib import asynccontextmanager

import bcrypt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import field_validator
from sqlmodel import Field, Session, SQLModel, UniqueConstraint, create_engine, select

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
    email: str
    password: str


class LoginUser(UserBase):
    pass


class User(UserBase):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    age: int


class UserCreate(User):
    repeat_password: str

    @field_validator("repeat_password")
    def repeat_password_must_match(v, values):
        if v != values.get("password"):
            raise HTTPException(
                status_code=400, detail="Repeat password does not match password."
            )
        return v


class UserTable(User, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"), UniqueConstraint("username"))
    id: Optional[int] = Field(default=None, primary_key=True)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(lifespan=lifespan)


@app.post("/register/", status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = UserTable.model_validate(user)
    session.add(db_user)
    session.commit()
    return {"id": db_user.id, "message": "User created successfully"}


@app.get("/users/")
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(UserTable)).all()
    return users


@app.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.exec(
        select(UserTable).where(UserTable.username == form_data.username)
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not bcrypt.checkpw(
        form_data.password.encode("utf-8"), db_user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"user": f"Eingeloggt als {db_user.username}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
