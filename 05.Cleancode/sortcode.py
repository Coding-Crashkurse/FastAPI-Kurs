from sqlalchemy import create_engine

import pydantic
import sqlmodel

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}