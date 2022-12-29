from typing import Optional

from pydantic import EmailStr

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


class CustomerIn(SQLModel):
    firstname: str
    lastname: str
    age: int
    email: EmailStr
    username: str
    password: str


class CustomerOut(SQLModel):
    customer_id: int
    firstname: str
    lastname: str
    age: int
    email: EmailStr
    username: str


class Customer(SQLModel, table=True):
    __tablename__ = "customer"
    customer_id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str
    age: int
    email: EmailStr
    username: str
    password: str

    purchases: list["Purchase"] = Relationship(back_populates="customer")


class Product(SQLModel, table=True):
    __tablename__ = "product"
    product_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: int

    purchases: list["Purchase"] = Relationship(back_populates="product")


class Purchase(SQLModel, table=True):
    __tablename__ = "purchase"
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    date: str

    product_id: Optional[int] = Field(default=None, foreign_key="product.product_id")
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.customer_id")

    product: Optional[Product] = Relationship(back_populates="purchases")
    customer: Optional[Customer] = Relationship(back_populates="purchases")
