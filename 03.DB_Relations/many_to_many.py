from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class PersonEbookLink(SQLModel, table=True):
    person_id: Optional[int] = Field(
        default=None, foreign_key="persons.id", primary_key=True
    )
    ebook_id: Optional[int] = Field(
        default=None, foreign_key="ebooks.id", primary_key=True
    )


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ebooks: list["Ebook"] = Relationship(
        back_populates="persons", link_model=PersonEbookLink
    )


class Ebook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    persons: list["Person"] = Relationship(
        back_populates="ebooks", link_model=PersonEbookLink
    )
