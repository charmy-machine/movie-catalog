from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    movie_title: str
    description: str
    rating_mpaa: str
    slug: str


class Movie(MovieBase):
    """Movie model"""

    pass


class MovieCreate(MovieBase):
    """Create movie model"""

    movie_title: Annotated[str, Len(3, 100)]
    description: Annotated[str, Len(3, 255)]
    rating_mpaa: Annotated[str, Len(1, 5)]
    slug: Annotated[str, Len(3, 10)]
