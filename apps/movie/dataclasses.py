from dataclasses import dataclass
from typing import List


@dataclass
class ShowTime:
    showtime: str
    format: str


@dataclass
class Movie:
    title: str
    showtimes: List[ShowTime]

    def get_showtimes(self):
        return self.showtimes

    def get_formatted_title(self):
        return self.title.upper().replace("-", " ")
