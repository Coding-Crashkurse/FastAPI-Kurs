from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    bücher_ids: Optional[int] = Field(default=None, foreign_key="buch.id")
    bücher: Optional["Buch"] = Relationship(back_populates="person")


class Buch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: str
    person: Optional["Person"] = Relationship(back_populates="bücher")
