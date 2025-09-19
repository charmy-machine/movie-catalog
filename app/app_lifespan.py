from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.movies.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions before app starts
    storage.init_storage_from_state()
    yield

    # Actions during app shutdown
