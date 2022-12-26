import uvicorn
from fastapi import FastAPI

app = FastAPI()

products = []


@app.get("/products")
async def get_products():
    return products


@app.post("/products")
async def create_product(product: dict):
    products.append(product)
    return {"success": "Product created"}


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: dict):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products[i] = product
            return {"success": "Product updated"}
    return {"error": "Product not found"}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products.pop(i)
            return {"success": "Product deleted"}
    return {"error": "Product not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
