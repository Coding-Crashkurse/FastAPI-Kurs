from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    führerschein_id: Optional[int] = Field(default=None, foreign_key="führerschein.id")
    führerschein: Optional["Führerschein"] = Relationship(back_populates="person")


class Führerschein(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: str
    person: Optional[Person] = Relationship(
        sa_relationship_kwargs={"uselist": False}, back_populates="führerschein"
    )
