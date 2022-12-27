import uvicorn
from fastapi import APIRouter, FastAPI, Request
import time
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout)  # write the logs to the console


app = FastAPI(title="Our Products API v1", version="0.1", description="API for our products")
router = APIRouter(tags=["Auth"])
router2 = APIRouter(tags=["Products"])

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logging.info(f'Process time in seconds: {process_time} für route {request.url.path}')
    return response


@router.get("/hello")
async def hello_world():
    return {"message": "Hello World"}


@router2.get("/hello2")
async def hello_world():
    return {"message": "Hello World2"}

@router2.get("/hello3")
async def hello_world():
    return {"message": "Hello World3"}

app.include_router(router)
app.include_router(router2)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
