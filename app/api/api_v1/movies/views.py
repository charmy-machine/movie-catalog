from typing import Annotated

from fastapi import Depends, APIRouter

from .crud import MOVIES_LIST
from .dependencies import prefetch_movie
from schemas.movie import Movie

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
