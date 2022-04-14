import json
from typing import Any, Dict, List

import requests

from apps.cinehoyts.constants import (
    CINEMAS,
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO_CENTRO,
    SANTIAGO_ORIENTE,
    SANTIAGO_PONIENTE,
    SANTIAGO_SUR,
    SUR_DE_CHILE,
)

CINEHOYTS_HOST = "https://cinehoyts.cl"


def get_zone_by_cinema(cinema):
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


def get_showings_by_zone(zone: str = "santiago-oriente") -> List[Dict[str, Any]]:
    try:
        payload = {"claveCiudad": zone, "esVIP": True}
        showings = requests.post(
            f"{CINEHOYTS_HOST}/Cartelera.aspx/GetNowPlayingByCity", json=payload
        )
        clean_showings = showings.json()
        return clean_showings["d"]["Cinemas"]
    except Exception:
        return []


def get_cinema_by_cinema_key(cinemas: List[Dict[str, Any]], cinema_key: str) -> Dict[str, Any]:
    for cinema in cinemas:
        if cinema["Key"] == cinema_key:
            return cinema
    return {}


def get_showtimes_by_date(
    cinemas: Dict[str, Any], date_name: str
) -> Dict[str, Any]:
    for date in cinemas["Dates"]:
        if date["ShowtimeDate"] == date_name:
            return date
    return {}


def get_movie_showings(movie_list: List[Dict[str, Any]], movie_title="batman"):
    for movie in movie_list:
        if movie_title in movie["Key"] or movie["Key"] in movie_title:
            return movie
    return {}


def get_showtimes(movie_showings):
    showings_text = ''
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format_name = formats["Name"]
        for show in showtimes:
            showtime = show["Time"]
            showings_text += f"{showtime} hrs, formato {format_name}\n"
    return showings_text


def get_showings(cinema: str, date: str, movie: str):
    zone = get_zone_by_cinema(cinema)
    cinema_showings = get_cinema_by_cinema_key(get_showings_by_zone(zone), cinema)
    if not cinema_showings:
        return ""
    cinema_name = cinema_showings["Name"]
    showtime_date = get_showtimes_by_date(cinema_showings, date.replace("-", " "))
    showtime_date_name = showtime_date["ShowtimeDate"]
    showtime_movies = showtime_date["Movies"]
    movie_showings = get_movie_showings(showtime_movies, movie)
    movie_title = movie_showings["Title"]
    showtime_result = f"{movie_title} está en {cinema_name} el {showtime_date_name} a las\n"
    showtime_result += get_showtimes(movie_showings)
    return showtime_result


def get_movie_showing_by_date(date: str, movie: str):
    date_formatted = date.replace("-", " ")
    total_showings = f'En {date_formatted} se están exhibiendo\n\n'
    for zone in CINEMAS.keys():
        zone_showings = get_showings_by_zone(zone)
        for cinema_key in CINEMAS[zone]:
            cinema = get_cinema_by_cinema_key(zone_showings, cinema_key)
            if not cinema:
                continue
            cinema_name = cinema['Name']
            total_showings += f'{cinema_name}\n\n'
            showtime_date = get_showtimes_by_date(cinema, date.replace("-", " "))
            showtime_movies = showtime_date["Movies"]
            movie_showings = get_movie_showings(showtime_movies, movie)
            if not movie_showings:
                return ''
            movie_title = movie_showings['Title']
            total_showings = f'{movie_title}\n'
            total_showings += get_showtimes(movie_showings)
            total_showings += '\n$SEPARATOR$\n\n'
        total_showings += '—————\n\n'
    return total_showings


def get_movie_showing_by_cinema(cinema: str, movie: str):
    zone = get_zone_by_cinema(cinema)
    cinema_showings = get_cinema_by_cinema_key(get_showings_by_zone(zone), cinema)
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    showtime_result = f"{cinema_name}\n\n"
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        showtime_movies = showtime_date["Movies"]
        movie_showings = get_movie_showings(showtime_movies, movie)
        movie_title = movie_showings["Title"]
        showtime_result += f"{movie_title} — {showtime_date_name}\n"
        showtime_result += get_showtimes(movie_showings)
        showtime_result += '—————\n\n$SEPARATOR$\n\n'
    return showtime_result


"""
def get_every_movie_showing(movie: str):
    zone = get_zone_by_cinema(cinema)
    cinemas = get_cinema_by_cinema_key(get_showings_by_zone(zone), cinema)
    showtime_date = get_showtimes_by_date(cinemas, date.replace("-", " "))
    showtime_movies = showtime_date["Movies"]
    movie_showings = get_movie_showings(showtime_movies, movie)
    return get_showtimes(
        movie_showings["Title"],
        cinemas["Name"],
        showtime_date["ShowtimeDate"],
        movie_showings,
    )
"""


def get_info_cities(zone):
    result = ""
    for city in CINEMAS[zone]:
        result += f"{city}\n"
    return result


def get_info_cinemas():
    result = ""
    for zone in CINEMAS.keys():
        for city in CINEMAS[zone]:
            result += f"{city}\n"
    return result
