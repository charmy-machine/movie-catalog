from typing import Annotated

from fastapi import Depends, APIRouter, status

from .crud import storage
from .dependencies import prefetch_movie
from schemas.movie import Movie, MovieCreate

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get("/", response_model=list[Movie])
def read_movies_list():
    return storage.get()


@router.get("/{slug}", response_model=Movie)
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
    return storage.create(movie_create)
