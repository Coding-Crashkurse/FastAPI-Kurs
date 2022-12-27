from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = []


class BaseProduct(BaseModel):
    name: str
    price: float


class Product(BaseProduct):
    id: int


class ResponseProduct(BaseProduct):
    pass


@app.get("/products", response_model=List[ResponseProduct], status_code=200)
async def get_products():
    return [ResponseProduct(**p.dict()) for p in products]


@app.post("/products", status_code=201)
async def create_product(product: Product):
    products.append(product)
    return {"success": "Product created"}


@app.get("/products/{product_id}", status_code=200)
async def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product.dict()
    return HTTPException(status_code=404, detail="Products not found")


@app.put("/products/{product_id}", status_code=200)
async def update_product(product_id: int, product: Product):
    for i, p in enumerate(products):
        if p.id == product_id:
            products[i] = product
            return {"success": "Product updated"}
    return HTTPException(status_code=404, detail="Products not found")


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p.id == product_id:
            products.pop(i)
            return
    return HTTPException(status_code=404, detail="Products not found")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
