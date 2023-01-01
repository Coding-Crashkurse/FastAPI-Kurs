import logging
import sys
import time

import uvicorn
from fastapi import APIRouter, FastAPI, Request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)  # write the logs to the console

description = """
Product App mit Login etc. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""


app = FastAPI()

router = APIRouter(tags=["Auth"])
router2 = APIRouter(tags=["Products"])


@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logging.info(
        f"Process time in seconds: {process_time} für route {request.url.path}"
    )
    return response


@router.get("/hello1")
async def hello_world1():
    return {"message": "Hello World1"}


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
