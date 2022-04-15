from typing import Any, Dict, List

import requests

from apps.cinehoyts.constants import (
    CINEMA_ZONES,
    CINEMAS,
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO_CENTRO,
    SANTIAGO_ORIENTE,
    SANTIAGO_PONIENTE,
    SANTIAGO_SUR,
    SUR_DE_CHILE,
)

CINEHOYTS_HOST = "https://cinehoyts.cl"


def _get_zone_by_cinema(cinema):
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


def is_chain(cinema):
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


def _get_movie_showings(movie_list: List[Dict[str, Any]], movie_title="batman"):
    for movie in movie_list:
        if movie_title in movie["Key"] or movie["Key"] in movie_title:
            return movie
    return {}


def _get_showtimes(movie_showings: Dict, format: str = None):
    showings_text = ""
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format_name = formats["Name"]
        if format_name != format:
            "NO HAY FUNCIONES EN ESTE FORMATO"
        for show in showtimes:
            showtime = show["Time"]
            showings_text += f"{showtime} hrs — {format_name}\n"
    return showings_text


def get_showings(movie: str, date: str, cinema: str):
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    if not cinema_showings:
        return ""
    cinema_name = cinema_showings["Name"]
    showtime_date = _get_showtimes_by_date(cinema_showings, date.replace("-", " "))
    showtime_date_name = showtime_date["ShowtimeDate"]
    showtime_movies = showtime_date["Movies"]
    movie_showings = _get_movie_showings(showtime_movies, movie)
    movie_title = movie_showings["Title"]
    showtime_result = f"{movie_title} — {cinema_name} — {showtime_date_name}\n"
    showtime_result += _get_showtimes(movie_showings)
    return showtime_result


def _get_formatted_showings_by_cinema(movie, date, cinema_key, zone_showings):
    cinema = _get_cinema_by_cinema_key(zone_showings, cinema_key)
    if not cinema:
        return ""
    cinema_name = cinema["Name"]
    showtime_date = _get_showtimes_by_date(cinema, date.replace("-", " "))
    showtime_movies = showtime_date["Movies"]
    movie_showings = _get_movie_showings(showtime_movies, movie)
    if not movie_showings:
        return ""
    total_showings = f"{cinema_name}\n"
    movie_title = movie_showings["Title"]
    total_showings += f"{movie_title}\n"
    total_showings += _get_showtimes(movie_showings)
    total_showings += "—————\n\n$SEPARATOR$\n\n"
    return total_showings


def _get_formatted_showings_by_zone(movie: str, date: str, zone: str):
    zone_showings = _get_showings_response_by_zone(zone)
    cinemas_in_zone = CINEMAS[zone]
    total_showings = ""
    for cinema_key in cinemas_in_zone:
        total_showings += _get_formatted_showings_by_cinema(
            movie, date, cinema_key, zone_showings
        )
    return total_showings


def get_showings_by_zone(movie: str, date: str, zone: str):
    date_formatted = date.replace("-", " ")
    total_showings = f"El {date_formatted} se están exhibiendo\n\n"
    total_showings += _get_formatted_showings_by_zone(movie, date, zone)
    return total_showings


def get_showing_by_date(movie: str, date: str):
    date_formatted = date.replace("-", " ")
    total_showings = f"En {date_formatted} se están exhibiendo\n\n"
    for zone in CINEMA_ZONES:
        total_showings += _get_formatted_showings_by_zone(movie, date, zone)
    return total_showings


def get_showing_by_cinema(movie: str, cinema: str, format: str = None):
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    showtime_result = f"{cinema_name}\n\n"
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        showtime_movies = showtime_date["Movies"]
        movie_showings = _get_movie_showings(showtime_movies, movie)
        if not movie_showings:
            continue
        movie_title = movie_showings["Title"]
        showtime_result += f"{movie_title} — {showtime_date_name}\n"
        showtime_result += _get_showtimes(movie_showings, format)
        showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def get_cinema_showings(cinema: str):
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    showtime_result = f"{cinema_name}\n\n"
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        showtime_movies = showtime_date["Movies"]
        showtime_result += f"{showtime_date_name}\n\n"
        for movie_showings in showtime_movies:
            movie_title = movie_showings["Title"]
            showtime_result += f"{movie_title}\n"
            showtime_result += f"{_get_showtimes(movie_showings)}\n"
        showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def get_cinema_showings_by_date(cinema: str, date: str):
    zone = _get_zone_by_cinema(cinema)
    cinema_showings = _get_cinema_by_cinema_key(
        _get_showings_response_by_zone(zone), cinema
    )
    cinema_name = cinema_showings["Name"]
    showtime_result = f"{cinema_name}\n\n"
    showtime_date = _get_showtimes_by_date(cinema_showings, date.replace("-", " "))
    showtime_movies = showtime_date["Movies"]
    for movie_showings in showtime_movies:
        movie_title = movie_showings["Title"]
        showtime_result += f"{movie_title}\n"
        showtime_result += _get_showtimes(movie_showings)
        showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def get_info_cities():
    result = ""
    for city in CINEMAS.keys():
        result += f"{city}\n"
    return result


def get_info_cinemas():
    result = ""
    for zone in CINEMAS.keys():
        for city in CINEMAS[zone]:
            result += f"{city}\n"
    return result
