from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    movie_title: str
    description: str
    rating_mpaa: str


class Movie(MovieBase):
    """Movie model"""

    movie_id: int


class MovieCreate(MovieBase):
    """Create movie model"""

    movie_title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    rating_mpaa: str = Field(..., min_length=1, max_length=5)
