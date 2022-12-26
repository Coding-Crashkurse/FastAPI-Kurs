from typing import Optional
from pydantic import BaseModel, validator


class Product(BaseModel):
    id: int
    name: str = None
    price: float
    tags: list[str] = []
    description: Optional[str] = None

    @validator("name")
    def name_must_be_capitalized(cls, v):
        if not v:
            raise ValueError("Name is required")
        if not v[0].isupper():
            raise ValueError("Name must be capitalized")
        return v


product = Product(id=1, name="apple", price=0.99, description="A red fruit")
print(product.id)
print(product.name)
product.tags = ["fruit", "red"]
product_dict = product.dict()
print(product_dict)
product2 = Product(**product_dict)
print(product2)
product3 = Product(id=2, name="banana", price=0.79)
