from typing import Annotated
from fastapi import FastAPI, Request, HTTPException, status, Depends

from schemas.movie import Movie

app = FastAPI(
    title="Movie Catalog",
)


MOVIES_LIST = [
    Movie(
        movie_id=1,
        movie_title="The Gentlemen",
        description="""Gangsters of all stripes share a drug farm. Guy Ritchie's swirling action comedy starring Matthew McConaughey and Hugh Grant""",
        rating_mpaa="R",
    ),
    Movie(
        movie_id=2,
        movie_title="Interstellar",
        description="""Humanity's next step will be the greatest""",
        rating_mpaa="PG-13",
    ),
]


@app.get("/")
def read_root(request: Request):
    docs_url = request.url.replace(path="/docs")
    return {"docs": str(docs_url)}


@app.get("/movies/", response_model=list[Movie])
def read_movies_list():
    return MOVIES_LIST


def prefetch_movie(movie_id: int) -> Movie | None:
    movie = next(
        (movie for movie in MOVIES_LIST if movie.movie_id == movie_id),
        None,
    )

    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id {movie_id} not found",
    )


@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie_details(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> Movie | None:
    return movie
