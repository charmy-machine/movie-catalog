from typing import Annotated

from fastapi import Depends, APIRouter, status

from .crud import MOVIES_LIST
from .dependencies import prefetch_movie
from schemas.movie import Movie, MovieCreate
from random import randint

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get("/", response_model=list[Movie])
def read_movies_list():
    return MOVIES_LIST


@router.get("/{movie_id}", response_model=Movie)
def read_movie_details(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> Movie | None:
    return movie


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate) -> Movie:
    return Movie(
        movie_id=randint(1, 9999),
        **movie_create.model_dump(),
    )
