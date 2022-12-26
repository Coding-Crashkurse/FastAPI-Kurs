import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

products = []


class Product(BaseModel):
    id: int
    name: str
    price: float


class ProductCreated(BaseModel):
    success: str
    product: Product


class ProductUpdated(BaseModel):
    success: str
    product: Product


# class ProductDeleted(BaseModel):
#     success: str


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product.dict()
    return {"error": "Product not found"}


# @app.get("/products")
# async def get_products():
#     return [p.dict() for p in products]


@app.get("/products", response_model=List[Product])
async def get_products():
    return products


@app.post("/products", response_model=ProductCreated)
async def create_product(product: Product):
    products.append(product)
    # return {"success": "Product created"}
    return ProductCreated(success="Product created", product=product)


@app.put("/products/{product_id}", response_model=ProductUpdated)
async def update_product(product_id: int, product: Product):
    for i, p in enumerate(products):
        if p.id == product_id:
            products[i] = product
            return ProductUpdated(success="Product updated", product=product)
    return {"error": "Product not found"}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p.id == product_id:
            products.pop(i)
            # return ProductDeleted(success="Product deleted")
    return {"error": "Product not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
