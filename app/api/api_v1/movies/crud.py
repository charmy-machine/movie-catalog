from pydantic import BaseModel

from schemas.movie import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie.slug] = movie
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

storage.create(
    MovieCreate(
        movie_title="The Gentlemen",
        description="Gangsters of all stripes share a drug farm. Guy Ritchie's swirling action comedy starring Matthew McConaughey and Hugh Grant",
        rating_mpaa="R",
        slug="1abc",
    )
)

storage.create(
    MovieCreate(
        movie_title="Interstellar",
        description="Humanity's next step will be the greatest",
        rating_mpaa="PG-13",
        slug="2abc",
    ),
)
