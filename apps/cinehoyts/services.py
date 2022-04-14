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


def get_zone_by_city(city):
    if city in NORTE_Y_CENTRO_DE_CHILE:
        return "norte-y-centro-de-chile"
    elif city in SANTIAGO_CENTRO:
        return "santiago-centro"
    elif city in SANTIAGO_ORIENTE:
        return "santiago-oriente"
    elif city in SANTIAGO_PONIENTE:
        return "santiago-poniente-y-norte"
    elif city in SANTIAGO_SUR:
        return "santiago-sur"
    elif city in SUR_DE_CHILE:
        return "sur-de-chile"
    return None


def get_showings_by_zone(zone: str = "santiago-oriente") -> List[Dict[str, Any]]:
    payload = {"claveCiudad": zone, "esVIP": True}
    showings = requests.post(
        f"{CINEHOYTS_HOST}/Cartelera.aspx/GetNowPlayingByCity", json=payload
    )
    clean_showings = showings.json()
    return clean_showings["d"]["Cinemas"]


def get_cinema_by_city(cinemas: List[Dict[str, Any]], city: str) -> Dict[str, Any]:
    for cinema in cinemas:
        if cinema["Key"] == city:
            return cinema
    return {}


def get_show_by_date(
    cinema_cities: List[Dict[str, Any]], date_name: str
) -> Dict[str, Any]:
    for date in cinema_cities["Dates"]:
        if date["ShowtimeDate"] == date_name:
            return date
    return {}


def get_movie(movie_list: List[Dict[str, Any]], movie_title="batman"):
    for movie in movie_list:
        if movie_title in movie["Key"] or movie["Key"] in movie_title:
            return movie
    return {}


def get_showings(city: str, date: str, movie: str):
    zone = get_zone_by_city(city)
    cinemas = get_showings_by_zone(zone)
    cinema_cities = get_cinema_by_city(cinemas, city)
    city_name = cinema_cities["Name"]
    showtime_date = get_show_by_date(cinema_cities, date.replace("-", " "))
    showtime_date_name = showtime_date["ShowtimeDate"]
    cinema_movies = showtime_date["Movies"]
    movie_showings = get_movie(cinema_movies, movie)
    movie_title = movie_showings["Title"]
    showings = []
    showings_text = f"{movie_title} está en {city_name} el {showtime_date_name} a las\n"
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format = formats["Name"]
        for show in showtimes:
            showtime = show["Time"]
            showings.append(
                {
                    "format": format,
                    "showtime": showtime,
                }
            )
            showings_text += f"{showtime} hrs, formato {format}\n"
    return showings_text


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
