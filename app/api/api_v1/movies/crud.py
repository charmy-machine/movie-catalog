from pydantic import BaseModel, ValidationError

from core.config import MOVIES_STORAGE_FILEPATH
from schemas.movie import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            return MovieStorage()
        return cls.model_validate_json(MOVIES_STORAGE_FILEPATH.read_text())

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie.slug] = movie
        self.save_state()
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self.save_state()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_state()
        return movie


try:
    storage = MovieStorage.from_state()
except ValidationError:
    storage = MovieStorage()
    storage.save_state()
