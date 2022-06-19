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
        formatted_showing_date = date["ShowtimeDate"].replace(" ", "-")
        day, month = formatted_showing_date.split("-")
        if int(day) < 10 and len(day) == 2:
            formatted_showing_date = formatted_showing_date[1:]
        formatted_searched_date = date_name.replace(" ", "-")
        if formatted_showing_date == formatted_searched_date:
            return date
    return {}


def _get_movie_showings(movie_list: List[Dict[str, Any]], movie_title="batman") -> Dict:
    for movie in movie_list:
        if movie_title in movie["Key"] or movie["Key"] in movie_title:
            return movie
    return {}


def _get_formatted_format(format: str):
    if format == 'ESP':
        return '2D ESP'
    if format == 'SUBT':
        return '2D SUB'
    format = format.replace('DOB', 'ESP')
    format = format.replace('SUBT', 'SUB')
    return format


def _get_showtimes(movie_showings: Dict, format: str = None) -> List[ShowTime]:
    total_showtimes = []
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format_name = _get_formatted_format(formats["Name"])
        if format and format not in format_name:
            continue
        for show in showtimes:
            showtime = show["Time"]
            total_showtimes.append(ShowTime(showtime=showtime, format=format_name))
    return total_showtimes


def get_showings(movie: str, date: str, cinema: str, format: str) -> ShowDate:
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
                    Movie(title=movie_title, showtimes=_get_showtimes(movie_showings, format))
                ],
            )
        ],
    )
    return showdate


def _get_formatted_showings_by_cinema(
    date, cinema_key, zone_showings, movie, format
) -> Optional[Cinema]:
    cinema = _get_cinema_by_cinema_key(zone_showings, cinema_key)
    if not cinema:
        return None
    showtime_date = _get_showtimes_by_date(cinema, date.replace("-", " "))
    if not showtime_date:
        return None
    movies = []
    for movie_showing in showtime_date["Movies"]:
        if not movie or (
            movie in movie_showing["Key"] or movie_showing["Key"] in movie
        ):
            movies.append(
                Movie(
                    title=movie_showing["Title"],
                    showtimes=_get_showtimes(movie_showing, format),
                )
            )
    cinema_showtimes = Cinema(name=cinema["Name"], movies=movies)
    return cinema_showtimes


def _get_formatted_showings_by_zone(
    date: str, zone: str, movie: str, format: str
) -> List[Cinema]:
    zone_showings = _get_showings_response_by_zone(zone)
    cinemas_in_zone = CINEMAS[zone]
    zone_showtimes = []
    for cinema_key in cinemas_in_zone:
        zone_showtime = _get_formatted_showings_by_cinema(
            date, cinema_key, zone_showings, movie, format
        )
        if not zone_showtime:
            continue
        zone_showtimes.append(zone_showtime)
    return zone_showtimes


def get_showings_by_zone(movie: str, date: str, zone: str, format: str) -> List[Cinema]:
    zone_showings = _get_showings_response_by_zone(zone)
    if zone not in CINEMAS:
        return []
    cinemas_in_zone = CINEMAS[zone]
    cinema_showtimes = []
    for cinema_key in cinemas_in_zone:
        cinema_showtime = _get_formatted_showings_by_cinema(
            date, cinema_key, zone_showings, movie, format
        )
        if not cinema_showtime:
            continue
        cinema_showtimes.append(cinema_showtime)
    return cinema_showtimes


def get_showing_by_date(movie: str, date: str, format: str) -> List[Cinema]:
    cinema_showtimes = []
    for zone in CINEMA_ZONES:
        cinema_showtime = _get_formatted_showings_by_zone(date, zone, movie, format)
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
                                showtimes=_get_showtimes(movie_showings, format),
                            )
                        ],
                    )
                ],
            )
        )
    return total_showings


def _get_movie_showtimes(showtime_movies: List[Dict[str, Any]], format: str) -> List[Movie]:
    movies = []
    for movie_showings in showtime_movies:
        movie_title = movie_showings["Title"]
        movies.append(
            Movie(title=movie_title, showtimes=_get_showtimes(movie_showings, format))
        )
    return movies


def get_cinema_showings(cinema: str, format: str) -> List[ShowDate]:
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    total_showings = []
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        movies = _get_movie_showtimes(showtime_date["Movies"], format)
        total_showings.append(
            ShowDate(
                date=showtime_date_name,
                cinemas=[Cinema(name=cinema_name, movies=movies)],
            )
        )
    return total_showings


def get_cinema_showings_by_date(cinema: str, date: str, format: str) -> ShowDate:
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    showtime_date = _get_showtimes_by_date(cinema_showings, date.replace("-", " "))
    showtime_date_name = showtime_date["ShowtimeDate"]
    movies = _get_movie_showtimes(showtime_date["Movies"], format)
    return ShowDate(
        date=showtime_date_name, cinemas=([Cinema(name=cinema_name, movies=movies)])
    )


def get_total(date: str, format: str) -> List[Cinema]:
    cinema_showtimes = []
    for zone in CINEMA_ZONES:
        cinema_showtime = _get_formatted_showings_by_zone(date, zone, "", format)
        if not cinema_showtime:
            continue
        cinema_showtimes += cinema_showtime
    return cinema_showtimes


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
