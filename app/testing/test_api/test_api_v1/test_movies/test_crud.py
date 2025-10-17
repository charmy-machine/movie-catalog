import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.movies.crud import storage
from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate

if getenv("TESTING") != "1":
    error_msg = "Environment is not ready for testing."
    raise OSError(error_msg)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def create_movie(self) -> Movie:
        movie_in = MovieCreate(
            movie_title="Some title",
            description="Some description",
            rating_mpaa="PG13",
            slug="".join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        )
        return storage.create_or_raise_if_exists(movie_in)

    def test_update(self) -> None:
        movie_update = MovieUpdate(
            **self.movie.model_dump(),
        )

        source_movie_description = self.movie.description
        movie_update.description *= 2

        updated_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )

        self.assertNotEqual(
            source_movie_description,
            movie_update.description,
        )

        self.assertEqual(
            movie_update,
            MovieUpdate(
                **updated_movie.model_dump(),
            ),
        )

    def test_update_partial(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description="Some new description",
        )

        source_movie_description = self.movie.description
        updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_partial_update,
        )

        self.assertNotEqual(
            source_movie_description,
            movie_partial_update.description,
        )

        self.assertEqual(
            movie_partial_update.description,
            updated_movie.description,
        )
