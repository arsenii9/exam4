from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime
import re
from typing import List
from pydantic import BaseModel, Field, field_validator
from Cinescope.constants_directory.roles import Roles

class Movie(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: str | None
    location: str
    published: bool
    genreId: int
    genre: dict
    createdAt: str
    rating: int


class MoviesResponse(BaseModel):
    movies: list[Movie]

    count: int
    page: int
    pageSize: int
    pageCount: int
