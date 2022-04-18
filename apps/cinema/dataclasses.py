from dataclasses import dataclass
from typing import List

from apps.movie.dataclasses import Movie


@dataclass
class Cinema:
    name: str
    movies: List[Movie]

    def get_movies(self):
        return self.movies


@dataclass
class ShowDate:
    date: str
    cinemas: List[Cinema]

    def get_cinemas(self):
        return self.cinemas

    def get_formatted_date(self):
        return self.date.replace("-", " ")

    def add_cinemas(self, cinemas):
        self.cinemas += cinemas
