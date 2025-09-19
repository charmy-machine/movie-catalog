import logging

from fastapi import HTTPException, status, BackgroundTasks, Request

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
