import logging

from pydantic import BaseModel
from redis import Redis

from core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB_MOVIES,
    REDIS_MOVIES_HASH_NAME,
)
from schemas.movie import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate

logger = logging.getLogger(__name__)

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB_MOVIES,
)


class MovieBaseError(Exception):
    """Base exception for movie CRUD actions."""


class MovieAlreadyExistsError(MovieBaseError):
    """Raised on movie creation if such slug already exists."""


class MovieStorage(BaseModel):
    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis.hvals(name=REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(name=REDIS_MOVIES_HASH_NAME, key=slug):
            return Movie.model_validate_json(data)
        return None

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(indent=2),
        )

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.save_movie(movie)
        logger.info("Created movie %s.", movie.movie_title)
        return movie

    def exists(self, slug: str) -> bool:
        return redis.hexists(
            name=REDIS_MOVIES_HASH_NAME,
            key=slug,
        )

    def create_or_raise_if_exists(self, movie_in: MovieCreate) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in)
        raise MovieAlreadyExistsError(movie_in.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(REDIS_MOVIES_HASH_NAME, slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


storage = MovieStorage()
