import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database
engine = create_engine("sqlite:///users.db")
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)


class UserModel(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    age: int


# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()


@app.post("/register/")
def create_user(user: UserModel):
    # Create a new user in the database using the provided user data
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    return {"id": new_user.id, "message": "User created successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
