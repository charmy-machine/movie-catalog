import logging

from fastapi import FastAPI, Request
from api import router as api_router

from core import config

logging.basicConfig(
    level=config.LOGGER_LEVEL,
    format=config.LOGGER_FORMAT,
)

app = FastAPI(title="Movie Catalog")

app.include_router(api_router)


@app.get("/")
def read_root(request: Request):
    docs_url = request.url.replace(path="/docs")
    return {"docs": str(docs_url)}
