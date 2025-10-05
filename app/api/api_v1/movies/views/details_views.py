from typing import Annotated

from fastapi import Depends, status, APIRouter, BackgroundTasks

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie import Movie, MovieUpdate, MoviePartialUpdate, MovieRead

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

MovieBySlug = Annotated[Movie, Depends(prefetch_movie)]


@router.get("/", response_model=MovieRead)
def read_movie_details(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> Movie | None:
    return movie


@router.put("/", response_model=MovieRead)
def update_movie_details(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_movie)
    return storage.update(movie=movie, movie_in=movie_in)


@router.patch("/", response_model=MovieRead)
def update_movie_details_partial(
    movie: MovieBySlug,
    movie_in: MoviePartialUpdate,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_movie)
    return storage.update_partial(movie=movie, movie_in=movie_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieBySlug,
    background_tasks: BackgroundTasks,
) -> None:
    background_tasks.add_task(storage.save_movie)
    storage.delete(movie=movie)
