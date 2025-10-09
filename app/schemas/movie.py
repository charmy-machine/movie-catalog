from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel


TitleString = Annotated[str, Len(3, 100)]
DescriptionString = Annotated[str, Len(3, 255)]
RatingString = Annotated[str, Len(1, 5)]


class MovieBase(BaseModel):
    movie_title: str
    description: str
    rating_mpaa: str


class MovieCreate(MovieBase):
    """Create movie model"""

    movie_title: TitleString
    description: DescriptionString
    rating_mpaa: RatingString
    slug: Annotated[str, Len(3, 10)]


class MovieUpdate(MovieBase):
    """Update movie model"""

    movie_title: TitleString
    description: DescriptionString
    rating_mpaa: RatingString


class MoviePartialUpdate(BaseModel):
    """Partial update movie model"""

    movie_title: TitleString | None = None
    description: DescriptionString | None = None
    rating_mpaa: RatingString | None = None


class MovieRead(MovieBase):
    """Read movie details model"""

    slug: str


class Movie(MovieBase):
    """Movie model"""

    slug: str
    notes: str = "some notes"
