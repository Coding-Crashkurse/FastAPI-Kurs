import uvicorn
from fastapi import FastAPI

description = """
Product App mit Login etc. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""


app = FastAPI(
    title="Our Product App API",
    version="1.0",
    description=description,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Our Product App Support Team",
        "url": "http://ourproductapp.com/contact/",
        "email": "support@ourproductapp.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
