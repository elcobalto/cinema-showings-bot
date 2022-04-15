from typing import Any, Dict, List

import requests

from apps.cinemark.constants import (
    CINEMA_ZONES,
    CINEMA_ZONES_TAGS,
    CINEMAS_TAGS,
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO,
    SUR_DE_CHILE,
)

CINEMARK_HOST = "https://api.cinemark.cl/api/"

month_to_number = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}


def is_chain(cinema):
    return cinema in CINEMAS_TAGS or cinema in CINEMA_ZONES_TAGS


def _get_cinema(cinema_name):
    for zone in CINEMA_ZONES:
        cinemas_in_zone = zone["list"]
        for cinema in cinemas_in_zone:
            if cinema_name == cinema["tag"]:
                return cinema
    return None


def _get_showings_response_by_zone(
    cinema_id: int = 512,
) -> List[Dict[str, Any]]:
    try:
        showings = requests.get(
            f"{CINEMARK_HOST}/vista/data/billboard?cinema_id={cinema_id}"
        )
        clean_showings = showings.json()
        return clean_showings
    except Exception:
        return []


def _check_date(date, dateshow):
    listed_date = date.split("-")
    listed_dateshow = dateshow["date"].split("-")
    month_date = listed_date[1]
    try:
        month = int(month_date)
    except Exception:
        month = month_to_number[month_date]
    return (
        int(month) == int(listed_dateshow[1])
        and int(listed_date[0]) == int(listed_dateshow[2])
    )


def _format_movieshow_title(movie_title):
    return movie_title.lower().replace(" ", "-")


def _check_similar_titles(movie, movie_title):
    return movie_title in movie or movie in movie_title


def _format_show_format(showformat):
    return showformat.split("(")[1][:-1]


def _get_formatted_showings_by_cinema(movie, movie_showings):
    showtime_result = ""
    for movie_showing in movie_showings:
        movie_title = _format_movieshow_title(movie_showing["title"])
        if not _check_similar_titles(movie, movie_title):
            continue
        movie_formats = movie_showing["movie_versions"]
        for show_format in movie_formats:
            format = _format_show_format(show_format["title"])
            for timeshow in show_format["sessions"]:
                showtime = timeshow["hour"]
                showtime_result += f"{showtime[:-3]} hrs — {format}\n"
    return showtime_result


def get_showings(movie: str, date: str, cinema_name: str):
    cinema = _get_cinema(cinema_name)
    dateshows = _get_showings_response_by_zone(cinema["id"])
    showtime_result = ""
    for dateshow in dateshows:
        is_date = _check_date(date, dateshow)
        if not is_date:
            continue
        showtime_result += f"{movie.upper()} — {cinema['name']} — {date}\n"
        showtime_result += _get_formatted_showings_by_cinema(movie, dateshow["movies"])
    return showtime_result


def _get_cinemas_by_zone(zone):
    for cinema_zone in CINEMA_ZONES:
        if cinema_zone["tag"] == zone:
            return cinema_zone["list"]
    return None


def _get_showings_by_cinema(movie, date, cinema):
    dateshows = _get_showings_response_by_zone(cinema["id"])
    showtime_result = f'{cinema["name"]}\n'
    for dateshow in dateshows:
        is_date = _check_date(date, dateshow)
        if not is_date:
            continue
        showtime_result += f'{movie.upper().replace("-", " ")}\n'
        showtime_result += _get_formatted_showings_by_cinema(movie, dateshow["movies"])
    showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def get_showings_by_zone(movie: str, date: str, zone: str):
    cinemas = _get_cinemas_by_zone(zone)
    showtime_result = f"El {date} se están exhibiendo\n\n"
    for cinema in cinemas:
        showtime_result += _get_showings_by_cinema(movie, date, cinema)
    return showtime_result


def get_showing_by_date(movie: str, date: str):
    showtime_result = f"El {date} se están exhibiendo\n\n"
    for cinema_tag in CINEMAS_TAGS:
        cinema = _get_cinema(cinema_tag)
        showtime_result += _get_showings_by_cinema(movie, date, cinema)
    return showtime_result


def get_showing_by_cinema(movie: str, cinema_name: str, format: str = None):
    cinema = _get_cinema(cinema_name)
    dateshows = _get_showings_response_by_zone(cinema["id"])
    showtime_result = f"{cinema['name']}\n\n"
    for dateshow in dateshows:
        showtime_result += f"{movie.upper()} — {dateshow['date']}\n"
        showtime_result += _get_formatted_showings_by_cinema(movie, dateshow["movies"])
        showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def _get_showtime_by_movieshowing(movie_showing):
    movie_title = _format_movieshow_title(movie_showing["title"])
    showtime_result = f"{movie_title.upper().replace('-', ' ')}\n"
    movie_formats = movie_showing["movie_versions"]
    for show_format in movie_formats:
        format = _format_show_format(show_format["title"])
        for timeshow in show_format["sessions"]:
            showtime = timeshow["hour"]
            showtime_result += f"{showtime[:-3]} hrs — {format}\n"
    return showtime_result


def get_cinema_showings(cinema_name: str):
    cinema = _get_cinema(cinema_name)
    dateshows = _get_showings_response_by_zone(cinema["id"])
    showtime_result = f'{cinema["name"]}\n\n'
    for dateshow in dateshows:
        showtime_result += f'{dateshow["date"]}\n\n'
        for movie_showing in dateshow["movies"]:
            showtime_result += _get_showtime_by_movieshowing(movie_showing)
            showtime_result += '\n'
        showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def get_cinema_showings_by_date(cinema_name: str, date: str):
    cinema = _get_cinema(cinema_name)
    dateshows = _get_showings_response_by_zone(cinema["id"])
    showtime_result = f'{cinema["name"]}\n\n'
    for dateshow in dateshows:
        is_date = _check_date(date, dateshow)
        if not is_date:
            continue
        for movie_showing in dateshow["movies"]:
            showtime_result += _get_showtime_by_movieshowing(movie_showing)
            showtime_result += "—————\n\n$SEPARATOR$\n\n"
    return showtime_result


def get_info_cities():
    result = ""
    for city in CINEMA_ZONES_TAGS:
        result += f"{city}\n"
    return result


def get_info_cinemas():
    result = ""
    for cinema in CINEMAS_TAGS:
        result += f"{cinema}\n"
    return result
