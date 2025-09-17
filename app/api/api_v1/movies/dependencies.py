from fastapi import HTTPException
from starlette import status

from .crud import MOVIES_LIST
from schemas.movie import Movie


def prefetch_movie(slug: str) -> Movie | None:
    movie = next(
        (item for item in MOVIES_LIST if item.slug == slug),
        None,
    )

    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug '{slug}' not found",
    )
