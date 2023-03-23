from typing import Any, Dict, List, Optional

import requests

from apps.cinema.constants.cinemark import (
    CINEMA_ZONES,
    CINEMA_ZONES_TAGS,
    CINEMAS_TAGS,
    TOTAL_CINEMAS_TAGS,
)
from apps.cinema.dataclasses import Cinema, ShowDate
from apps.movie.dataclasses import Movie, ShowTime

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


def is_chain(cinema: str) -> bool:
    """

    :param cinema:
    :return:
    """
    return cinema in CINEMAS_TAGS or cinema in CINEMA_ZONES_TAGS


def get_cinema_by_cinema_tag(cinema_tag: str) -> Optional[Dict[str, Any]]:
    """

    :param cinema_tag:
    :return:
    """
    for zone in CINEMA_ZONES:
        cinemas_in_zone = zone["list"]
        for cinema in cinemas_in_zone:
            if cinema_tag == cinema["tag"]:
                return cinema
    return None


def _get_showings_response_by_zone(
    cinema_id: int = 512,
) -> List[Dict[str, Any]]:
    """

    :param cinema_id:
    :return:
    """
    try:
        showings = requests.get(
            f"{CINEMARK_HOST}/vista/data/billboard?cinema_id={cinema_id}"
        )
        clean_showings = showings.json()
        return clean_showings
    except Exception:
        return []


def _check_date(date: str, dateshow: Dict[str, Any]) -> bool:
    """

    :param date:
    :param dateshow:
    :return:
    """
    if not date:
        return True
    listed_date = date.split("-")
    listed_dateshow = dateshow["date"].split("-")
    month_date = listed_date[1]
    try:
        month = int(month_date)
    except Exception:
        month = month_to_number[month_date]
    return int(month) == int(listed_dateshow[1]) and int(listed_date[0]) == int(
        listed_dateshow[2]
    )


def _format_movieshow_title(movie_title: str) -> str:
    """

    :param movie_title:
    :return:
    """
    return movie_title.lower().replace(" ", "-")


def _check_similar_titles(first_movie: str, second_movie: str) -> bool:
    """

    :param first_movie:
    :param second_movie:
    :return:
    """
    return second_movie in first_movie or first_movie in second_movie


def _format_show_format(show_format: str) -> str:
    """

    :param show_format:
    :return:
    """
    return show_format.split("(")[1][:-1].replace("DOB", "ESP").replace("SUBT", "SUB")


def _get_movie_showtimes(
    movie_title: str, movie_showing: Dict[str, Any], show_format: str
) -> Movie:
    """

    :param movie_title:
    :param movie_showing:
    :param show_format:
    :return:
    """
    movie_formats = movie_showing["movie_versions"]
    showtimes = []
    for show_format_data in movie_formats:
        show_format_title = show_format_data["title"]
        show_format_sessions = show_format_data["sessions"]
        format_name = _format_show_format(show_format=show_format_title)
        if show_format and show_format not in format_name:
            continue
        for timeshow in show_format_sessions:
            showtime = timeshow["hour"]
            showtimes.append(
                ShowTime(
                    showtime=showtime[:-3],
                    format=format_name,
                    seats=timeshow["seats_available"],
                )
            )
    return Movie(title=movie_title, showtimes=showtimes)


def _get_formatted_movie_showings(
    movie_showings: List[Dict[str, Any]],
    movie_tag: str,
    show_format: str,
) -> List[Movie]:
    """

    :param movie_showings:
    :param movie_tag:
    :param show_format:
    :return:
    """
    movies = []
    for movie_showing in movie_showings:
        movie_title = _format_movieshow_title(movie_title=movie_showing["title"])
        if movie_tag and not _check_similar_titles(
            first_movie=movie_tag, second_movie=movie_title
        ):
            continue
        movies.append(
            _get_movie_showtimes(
                movie_title=movie_title,
                movie_showing=movie_showing,
                show_format=show_format,
            )
        )
    return movies


def get_showings(
    movie_tag: str, date: str, cinema_tag: str, format: str
) -> List[ShowDate]:
    """

    :param movie_tag:
    :param date:
    :param cinema_tag:
    :param format:
    :return:
    """
    total: Dict[str, Dict[str, List[Movie]]] = {}
    for zone in CINEMA_ZONES:
        cinemas_in_zone = zone["list"]
        for cinema in cinemas_in_zone:
            if cinema_tag and cinema_tag == cinema["tag"]:
                continue
            dateshows = _get_showings_response_by_zone(cinema_id=cinema["id"])
            cinemas = []
            for dateshow in dateshows:
                is_date = _check_date(date=date, dateshow=dateshow)
                if not is_date:
                    continue
                showtime_date_name = dateshow["date"]
                movies = _get_formatted_movie_showings(
                    movie_showings=dateshow["movies"],
                    movie_tag=movie_tag,
                    show_format=format,
                )
                cinemas.append(Cinema(name=cinema["name"], movies=movies))
                cinema_name = cinema["name"]
                if (
                    showtime_date_name not in total
                    or cinema_name not in total[showtime_date_name]
                ):
                    total[showtime_date_name] = {cinema_name: movies}
                else:
                    total[showtime_date_name][cinema_name] += movies
    showdates = []
    for showtime in total.keys():
        cinemas = []
        for cinema in total[showtime].keys():
            cinemas.append(Cinema(name=cinema, movies=total[showtime][cinema]))
        showdates.append(ShowDate(date=showtime, cinemas=cinemas))
    return showdates


def _get_cinemas_by_zone(zone: str) -> List[Dict[str, Any]]:
    """

    :param zone:
    :return:
    """
    for cinema_zone in CINEMA_ZONES:
        if cinema_zone["tag"] == zone:
            return cinema_zone["list"]
    return []


def _get_showings_by_cinema(
    date: str, cinema: Dict[str, Any], movie: str, format: str
) -> List[Cinema]:
    """

    :param date:
    :param cinema:
    :param movie:
    :param format:
    :return:
    """
    dateshows = _get_showings_response_by_zone(cinema_id=cinema["id"])
    cinemas = []
    for dateshow in dateshows:
        is_date = _check_date(date=date, dateshow=dateshow)
        if not is_date:
            continue
        movies = _get_formatted_movie_showings(
            movie_showings=dateshow["movies"], movie_tag=movie, show_format=format
        )
        cinemas.append(
            Cinema(
                name=cinema["name"],
                movies=movies,
            )
        )
    return cinemas


def get_showings_by_cinema_tags(
    movie: str, date: str, cinemas: List[Dict[str, Any]], format: str
) -> List[ShowDate]:
    """

    :param movie:
    :param date:
    :param cinemas:
    :param format:
    :return:
    """
    cinemas_showdates = []
    for cinema in cinemas:
        cinemas_showdates += get_showings(
            movie_tag=movie, date=date, cinema_tag=cinema["name"], format=format
        )
    return cinemas_showdates


def get_showings_by_zone(
    movie: str, date: str, zone_name: str, format: str
) -> List[ShowDate]:
    """

    :param movie:
    :param date:
    :param zone_name:
    :param format:
    :return:
    """
    return get_showings_by_cinema_tags(
        movie=movie,
        date=date,
        cinemas=_get_cinemas_by_zone(zone=zone_name),
        format=format,
    )


def _get_movie_showtimes_for_movie_showings(dateshow: Dict, format: str) -> List[Movie]:
    """

    :param dateshow:
    :param format:
    :return:
    """
    movie_showtimes = []
    for movie_showing in dateshow["movies"]:
        movie_title = _format_movieshow_title(movie_title=movie_showing["title"])
        movie_showtimes.append(
            _get_movie_showtimes(
                movie_title=movie_title, movie_showing=movie_showing, show_format=format
            )
        )
    return movie_showtimes


def get_cinema_showings(cinema: Dict[str, Any], format: str) -> List[ShowDate]:
    """

    :param cinema:
    :param format:
    :return:
    """
    dateshows = _get_showings_response_by_zone(cinema_id=cinema["id"])
    showdates = []
    for dateshow in dateshows:
        movies = _get_movie_showtimes_for_movie_showings(
            dateshow=dateshow, format=format
        )
        showdates.append(
            ShowDate(
                date=dateshow["date"],
                cinemas=[Cinema(name=cinema["name"], movies=movies)],
            )
        )
    return showdates


def get_cinema_showings_by_date(
    cinema: Dict[str, Any], date: str, format: str
) -> ShowDate:
    """

    :param cinema:
    :param date:
    :param format:
    :return:
    """
    dateshows = _get_showings_response_by_zone(cinema_id=cinema["id"])
    movies = []
    for dateshow in dateshows:
        is_date = _check_date(date=date, dateshow=dateshow)
        if not is_date:
            continue
        movies += _get_movie_showtimes_for_movie_showings(
            dateshow=dateshow, format=format
        )
    return ShowDate(
        date=dateshows[0]["date"], cinemas=[Cinema(name=cinema["name"], movies=movies)]
    )


def get_total(date: str, format: str) -> List[Cinema]:
    """

    :param date:
    :param format:
    :return:
    """
    cinemas_showdates = []
    for cinema_tag in TOTAL_CINEMAS_TAGS:
        cinema = get_cinema_by_cinema_tag(cinema_tag=cinema_tag)
        cinemas_showdates += _get_showings_by_cinema(
            date=date, cinema=cinema, movie="", format=format
        )
    return cinemas_showdates
