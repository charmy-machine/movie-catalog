from unittest import TestCase

from pydantic import ValidationError

from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate

movie = MovieCreate(
    movie_title="Some Title",
    description="Some Description",
    rating_mpaa="PG13",
    slug="some-slug",
)


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = Movie(**movie.model_dump())

        self.assertEqual(movie_in.movie_title, movie.movie_title)
        self.assertEqual(movie_in.rating_mpaa, movie.rating_mpaa)
        self.assertEqual(movie_in.rating_mpaa, movie.rating_mpaa)
        self.assertEqual(movie_in.slug, movie.slug)

    def test_movie_create_accepts_different_titles(self) -> None:
        titles = [
            "Some Long Title",
            "Ttl",
        ]

        for title in titles:
            with self.subTest(title=title, msg=f"title {title}"):
                movie_in = MovieCreate(
                    movie_title=title,
                    description="Some Description",
                    rating_mpaa="PG13",
                    slug="some-slug",
                )

                self.assertEqual(
                    title,
                    movie_in.model_dump(mode="json")["movie_title"],
                )

    def test_movie_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            _ = MovieCreate(
                movie_title="Some Title",
                description="Some Description",
                rating_mpaa="PG13",
                slug="s",
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(
            expected_type,
            error_details["type"],
        )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_update_schema(self) -> None:
        movie_in = MovieUpdate(
            movie_title="Some New Title",
            description="Some New Description",
            rating_mpaa="PG15",
        )

        for field_name, value in movie_in:
            setattr(movie, field_name, value)

        self.assertEqual(movie_in.movie_title, movie.movie_title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.rating_mpaa, movie.rating_mpaa)


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_partial_updated_from_update_schema(self) -> None:
        movie_in = MoviePartialUpdate(description="abc")

        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)

        self.assertEqual(movie_in.description, movie.description)
