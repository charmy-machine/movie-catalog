import logging

from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from app_lifespan import lifespan
from core import config

logging.basicConfig(
    level=config.LOGGER_LEVEL,
    format=config.LOGGER_FORMAT,
)

app = FastAPI(
    title="Movie Catalog",
    lifespan=lifespan,
)

app.include_router(main_router)
app.include_router(api_router)
