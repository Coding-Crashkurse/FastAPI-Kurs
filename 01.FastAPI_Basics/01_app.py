import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
