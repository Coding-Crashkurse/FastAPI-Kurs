import uvicorn
from fastapi import APIRouter, FastAPI

app = FastAPI(
    title="Our Products API v1", version="0.1", description="API for our products"
)
router = APIRouter(tags=["Auth"])
router2 = APIRouter(tags=["Products"])


@router.get("/hello")
def hello_world():
    return {"message": "Hello World"}


@router2.get("/hello2")
def hello_world():
    return {"message": "Hello World2"}


@router2.get("/hello3")
def hello_world():
    return {"message": "Hello World3"}


app.include_router(router)
app.include_router(router2)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
