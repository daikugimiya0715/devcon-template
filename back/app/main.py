import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import llm
from app.utils.logger import configure_logger, logger

load_dotenv()


configure_logger()


app = FastAPI()
app.include_router(llm.router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple message."""
    return {"message": "Hello, World!"}
