from typing import Annotated

from fastapi import Depends, status, APIRouter

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie import Movie

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": f"Movie with slug 'slug' not found.",
                    },
                },
            },
        },
    },
)


@router.get("/", response_model=Movie)
def read_movie_details(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> Movie | None:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(item: Annotated[Movie, Depends(prefetch_movie)]) -> None:
    storage.delete(movie=item)
