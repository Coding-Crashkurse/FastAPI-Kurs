import uvicorn
from db_and_models.models import Customer, CustomerIn, CustomerOut, Product, Purchase
from db_and_models.session import create_db_and_tables, drop_tables, get_session
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/register/")
def register(customer: CustomerIn, db: Session = Depends(get_session)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.post("/products/")
def create_product(product: Product, db: Session = Depends(get_session)):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_session)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}")
def update_product(
    product_id: int, product: Product, db: Session = Depends(get_session)
):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product.dict(exclude_unset=True)
    db_product.update(update_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_session)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Successfully deleted product"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
def on_shutdown():
    drop_tables()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
