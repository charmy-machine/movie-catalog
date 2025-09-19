import logging
from typing import Annotated

from fastapi import HTTPException, status, BackgroundTasks, Request, Header

from core.config import API_TOKENS
from .crud import storage
from schemas.movie import Movie

logger = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def prefetch_movie(slug: str) -> Movie | None:
    movie = storage.get_by_slug(slug)

    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug '{slug}' not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    # Code BEFORE enter inside the view function
    yield
    # Code AFTER exiting the view function
    if request.method in UNSAFE_METHODS:
        logger.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[str, Header(alias="x-auth-token")] = "",
):
    if request.method not in UNSAFE_METHODS:
        return

    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
