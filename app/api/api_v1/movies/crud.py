import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core.config import (
    MOVIES_STORAGE_FILEPATH,
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


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        logger.info("Saved movies to storage file.")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            logger.info("Storage file doesn't exist.")
            return MovieStorage()
        return cls.model_validate_json(MOVIES_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = self.from_state()
        except ValidationError:
            self.save_state()
            logger.info("Rewritten storage file due to validation error.")
            return

        self.slug_to_movie.update(data.slug_to_movie)

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())

        redis.hset(
            name=REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(indent=2),
        )

        logger.info("Created movie %s.", movie)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        return movie


storage = MovieStorage()
