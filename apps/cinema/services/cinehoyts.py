from typing import Any, Dict, List, Optional

import requests

from apps.cinema.constants.cinehoyts import (
    CINEMA_ZONES,
    CINEMAS,
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO_CENTRO,
    SANTIAGO_ORIENTE,
    SANTIAGO_PONIENTE,
    SANTIAGO_SUR,
    SUR_DE_CHILE,
)
from apps.cinema.dataclasses import Cinema, ShowDate
from apps.movie.dataclasses import Movie, ShowTime

CINEHOYTS_HOST = "https://cinehoyts.cl"


def _get_zone_by_cinema(cinema: str) -> Optional[str]:
    if cinema in NORTE_Y_CENTRO_DE_CHILE:
        return "norte-y-centro-de-chile"
    elif cinema in SANTIAGO_CENTRO:
        return "santiago-centro"
    elif cinema in SANTIAGO_ORIENTE:
        return "santiago-oriente"
    elif cinema in SANTIAGO_PONIENTE:
        return "santiago-poniente-y-norte"
    elif cinema in SANTIAGO_SUR:
        return "santiago-sur"
    elif cinema in SUR_DE_CHILE:
        return "sur-de-chile"
    return None


def is_chain(cinema: str) -> bool:
    zone = _get_zone_by_cinema(cinema)
    return zone is not None


def _get_showings_response_by_zone(
    zone: str = "santiago-oriente",
) -> List[Dict[str, Any]]:
    try:
        payload = {"claveCiudad": zone, "esVIP": True}
        showings = requests.post(
            f"{CINEHOYTS_HOST}/Cartelera.aspx/GetNowPlayingByCity", json=payload
        )
        clean_showings = showings.json()
        return clean_showings["d"]["Cinemas"]
    except Exception:
        return []


def _get_cinema_by_cinema_key(
    cinemas: List[Dict[str, Any]], cinema_key: str
) -> Dict[str, Any]:
    for cinema in cinemas:
        if cinema["Key"] == cinema_key:
            return cinema
    return {}


def _get_showtimes_by_date(cinemas: Dict[str, Any], date_name: str) -> Dict[str, Any]:
    for date in cinemas["Dates"]:
        if date["ShowtimeDate"] == date_name:
            return date
    return {}


def _get_movie_showings(movie_list: List[Dict[str, Any]], movie_title="batman") -> Dict:
    for movie in movie_list:
        if movie_title in movie["Key"] or movie["Key"] in movie_title:
            return movie
    return {}


def _get_showtimes(movie_showings: Dict, format: str = None) -> List[ShowTime]:
    total_showtimes = []
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format_name = formats["Name"]
        if format and format_name != format:
            continue
        for show in showtimes:
            showtime = show["Time"]
            total_showtimes.append(ShowTime(showtime=showtime, format=format_name))
    return total_showtimes


def get_showings(movie: str, date: str, cinema: str) -> ShowDate:
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    if not cinema_showings:
        return None
    cinema_name = cinema_showings["Name"]
    showtime_date = _get_showtimes_by_date(cinema_showings, date)
    showtime_date_name = showtime_date["ShowtimeDate"]
    showtime_movies = showtime_date["Movies"]
    movie_showings = _get_movie_showings(showtime_movies, movie)
    movie_title = movie_showings["Title"]
    showdate = ShowDate(
        date=showtime_date_name,
        cinemas=[
            Cinema(
                name=cinema_name,
                movies=[
                    Movie(title=movie_title, showtimes=_get_showtimes(movie_showings))
                ],
            )
        ],
    )
    return showdate


def _get_formatted_showings_by_cinema(
    movie, date, cinema_key, zone_showings
) -> Optional[Cinema]:
    cinema = _get_cinema_by_cinema_key(zone_showings, cinema_key)
    if not cinema:
        return None
    showtime_date = _get_showtimes_by_date(cinema, date.replace("-", " "))
    if not showtime_date:
        return None
    movie_showings = _get_movie_showings(showtime_date["Movies"], movie)
    if not movie_showings:
        return None
    cinema_showtimes = Cinema(
        name=cinema["Name"],
        movies=[
            Movie(
                title=movie_showings["Title"], showtimes=_get_showtimes(movie_showings)
            )
        ],
    )
    return cinema_showtimes


def _get_formatted_showings_by_zone(movie: str, date: str, zone: str) -> List[Cinema]:
    zone_showings = _get_showings_response_by_zone(zone)
    cinemas_in_zone = CINEMAS[zone]
    zone_showtimes = []
    for cinema_key in cinemas_in_zone:
        zone_showtime = _get_formatted_showings_by_cinema(
            movie, date, cinema_key, zone_showings
        )
        if not zone_showtime:
            continue
        zone_showtimes.append(zone_showtime)
    return zone_showtimes


def get_showings_by_zone(movie: str, date: str, zone: str) -> List[Cinema]:
    zone_showings = _get_showings_response_by_zone(zone)
    if zone not in CINEMAS:
        return []
    cinemas_in_zone = CINEMAS[zone]
    cinema_showtimes = []
    for cinema_key in cinemas_in_zone:
        cinema_showtime = _get_formatted_showings_by_cinema(
            movie, date, cinema_key, zone_showings
        )
        if not cinema_showtime:
            continue
        cinema_showtimes.append(cinema_showtime)
    return cinema_showtimes


def get_showing_by_date(movie: str, date: str) -> List[Cinema]:
    cinema_showtimes = []
    for zone in CINEMA_ZONES:
        cinema_showtime = _get_formatted_showings_by_zone(movie, date, zone)
        if not cinema_showtime:
            continue
        cinema_showtimes += cinema_showtime
    return cinema_showtimes


def get_showing_by_cinema(
    movie: str, cinema: str, format: str = None
) -> List[ShowDate]:
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    total_showings = []
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        showtime_movies = showtime_date["Movies"]
        movie_showings = _get_movie_showings(showtime_movies, movie)
        if not movie_showings:
            continue
        movie_title = movie_showings["Title"]
        total_showings.append(
            ShowDate(
                date=showtime_date_name,
                cinemas=[
                    Cinema(
                        name=cinema_name,
                        movies=[
                            Movie(
                                title=movie_title,
                                showtimes=_get_showtimes(movie_showings),
                            )
                        ],
                    )
                ],
            )
        )
    return total_showings


def _get_movie_showtimes(showtime_movies: List[Dict[str, Any]]) -> List[Movie]:
    movies = []
    for movie_showings in showtime_movies:
        movie_title = movie_showings["Title"]
        movies.append(
            Movie(title=movie_title, showtimes=_get_showtimes(movie_showings))
        )
    return movies


def get_cinema_showings(cinema: str) -> List[ShowDate]:
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    total_showings = []
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        movies = _get_movie_showtimes(showtime_date["Movies"])
        total_showings.append(
            ShowDate(
                date=showtime_date_name,
                cinemas=[Cinema(name=cinema_name, movies=movies)],
            )
        )
    return total_showings


def get_cinema_showings_by_date(cinema: str, date: str) -> ShowDate:
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    showtime_date = _get_showtimes_by_date(cinema_showings, date.replace("-", " "))
    showtime_date_name = showtime_date["ShowtimeDate"]
    movies = _get_movie_showtimes(showtime_date["Movies"])
    return ShowDate(
        date=showtime_date_name, cinemas=([Cinema(name=cinema_name, movies=movies)])
    )


def get_info_cities() -> str:
    result = ""
    for city in CINEMAS.keys():
        result += f"{city}\n"
    return result


def get_info_cinemas() -> str:
    result = ""
    for zone in CINEMAS.keys():
        for city in CINEMAS[zone]:
            result += f"{city}\n"
    return result