from pydantic import BaseModel


class MovieBase(BaseModel):
    movie_id: int
    movie_title: str
    description: str
    rating_mpaa: str


class Movie(MovieBase):
    """Movie model"""

    pass
