from typing import Any, Dict, List, Optional, Tuple

import requests

from apps.cinema.constants.cinehoyts import (
    CINEMA_CITIES,
    CINEMA_ZONES,
    CINEMAS,
    CINEMAS_SANTIAGO,
    NORTE_Y_CENTRO_DE_CHILE_TAGS,
    SANTIAGO_CENTRO_TAGS,
    SANTIAGO_NORTE_Y_PONIENTE_TAGS,
    SANTIAGO_ORIENTE_TAGS,
    SANTIAGO_SUR_TAGS,
    SUR_DE_CHILE_TAGS,
)
from apps.cinema.dataclasses import Cinema, ShowDate
from apps.movie.dataclasses import Movie, ShowTime

CINEHOYTS_HOST = "https://cinehoyts.cl"


def _get_zone_by_cinema(cinema: str) -> Optional[str]:
    """
    Gets a zone tag from a cinema tag. Returns None for a not mapped zone tag.
    :param cinema: cinema tag.
    :return: Zone tag.
    """
    if cinema in NORTE_Y_CENTRO_DE_CHILE_TAGS:
        return "norte-y-centro-de-chile"
    elif cinema in SANTIAGO_CENTRO_TAGS:
        return "santiago-centro"
    elif cinema in SANTIAGO_ORIENTE_TAGS:
        return "santiago-oriente"
    elif cinema in SANTIAGO_NORTE_Y_PONIENTE_TAGS:
        return "santiago-poniente-y-norte"
    elif cinema in SANTIAGO_SUR_TAGS:
        return "santiago-sur"
    elif cinema in SUR_DE_CHILE_TAGS:
        return "sur-de-chile"
    return None


def is_chain(cinema: str) -> bool:
    """
    Determines if a cinema belongs to the CineHoyts chain.
    :param cinema: Cinema tag.
    :return: Descriptor if a cinema is from CineHoyts.
    """
    zone = _get_zone_by_cinema(cinema=cinema)
    return zone is not None


def _get_showings_response_by_zone(
    zone: str = "santiago-oriente",
) -> List[Dict[str, Any]]:
    """
    Gets showings response from a zone tag.
    :param zone: Zone tag.
    :return: Showings response.
    """
    try:
        payload = {"claveCiudad": zone, "esVIP": True}
        showings = requests.post(
            f"{CINEHOYTS_HOST}/Cartelera.aspx/GetNowPlayingByCity", json=payload
        )
        clean_showings = showings.json()
        return clean_showings["d"]["Cinemas"]
    except Exception:
        return []


def _get_cinemas_by_zone(zone: str) -> List[Dict[str, Any]]:
    """
    Gets a cinema dataclass list from a general zone name.
    :param zone_name: Zone name.
    :return: List of cinema dataclasses.
    """
    for cinema_zone in CINEMA_ZONES:
        if cinema_zone["tag"] == zone:
            return cinema_zone["list"]
    return []


def _get_showings_from_specific_cinemas(
    cinema_showings: List[Dict[str, Any]], cinemas: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Gets reduced showings from a list of specific cinemas.
    :param cinema_showings: List of unreduced cinema showings.
    :param cinemas: List of cinemas.
    :return: List of reduced cinema showings.
    """
    reduced_cinema_showings = []
    for cinema_showing in cinema_showings:
        for cinema in cinemas:
            if cinema_showing["Key"] == cinema["id"]:
                reduced_cinema_showings.append(cinema_showing)
    return reduced_cinema_showings


def get_cinema_by_cinema_tag(cinema_name: str) -> Optional[Dict[str, Any]]:
    """
    Gets a cinema dataclass object from a cinema name tag.
    :param cinema_name: Cinema name tag.
    :return: Cinema dataclass object.
    """
    for zone in CINEMA_ZONES:
        cinemas_in_zone = zone["list"]
        for cinema in cinemas_in_zone:
            if cinema_name == cinema["tag"]:
                return cinema
    return None


def get_showing_by_cinemas_and_cinema_tag(
    showings: List[Dict[str, Any]], cinema_tag: str
) -> Dict[str, Any]:
    """
    Gets a cinema dataclass object from cinema list and to be searched cinema tag.
    :param showings: List of cinema dataclass objects.
    :param cinema_tag: Cinema tag to be searched.
    :return: Searched cinema dataclass object.
    """
    for cinema_showing in showings:
        if cinema_showing["Key"] == cinema_tag:
            return cinema_showing
    return {}


def _get_showtime_by_date(showing: Dict[str, Any], date_name: str) -> Dict[str, Any]:
    """
    Gets cinema showtimes by an specific date.
    :param showing: Cinema with showtimes.
    :param date_name: Date to be searched.
    :return: Cinema showtime.
    """
    for showtime_date in showing["Dates"]:
        formatted_showtime_date = showtime_date["ShowtimeDate"].replace(" ", "-")
        day, month = formatted_showtime_date.split("-")
        if int(day) < 10 and len(day) == 2:
            formatted_showtime_date = formatted_showtime_date[1:]
        formatted_searched_date = date_name.replace(" ", "-")
        if formatted_showtime_date == formatted_searched_date:
            return showtime_date
    return {}


def _get_movie_showings(movie_list: List[Dict[str, Any]], movie_title: str) -> Dict:
    """
    Gets movie showings from list of movies with a to be searched movie title.
    :param movie_list: List of movie showings.
    :param movie_title: Movie title.
    :return: Movie showings.
    """
    for movie in movie_list:
        if movie_title in movie["Key"] or movie["Key"] in movie_title:
            return movie
    return {}


def _get_formatted_format(format: str):
    """
    Formats a showtime format.
    :param format: Showtime format.
    :return: Formatted showtime format.
    """
    if format == "ESP":
        return "2D ESP"
    if format == "SUBT":
        return "2D SUB"
    format = format.replace("DOB", "ESP")
    format = format.replace("SUBT", "SUB")
    return format


def _get_showtimes(movie_showings: Dict, format: str = None) -> List[ShowTime]:
    """
    Gets list of showtimes dataclasses objects from movie showings. Filtered by format if given.
    :param movie_showings: Movie showings.
    :param format: Optional showtime format.
    :return: List of showtimes dataclasses objects.
    """
    total_showtimes = []
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format_name = _get_formatted_format(format=formats["Name"])
        if format and format not in format_name:
            continue
        for show in showtimes:
            showtime = show["Time"]
            total_showtimes.append(ShowTime(showtime=showtime, format=format_name, seats=""))
    return total_showtimes


def get_showings(movie: str, date: str, cinema: str, format: str) -> Optional[ShowDate]:
    """

    :param movie:
    :param date:
    :param cinema:
    :param format:
    :return:
    """
    zone = _get_zone_by_cinema(cinema=cinema)
    cinema_showing = get_showing_by_cinemas_and_cinema_tag(
        showings=_get_showings_response_by_zone(zone=zone), cinema_tag=cinema
    )
    if not cinema_showing:
        return None
    cinema_name = cinema_showing["Name"]
    showtime_date = _get_showtime_by_date(showing=cinema_showing, date_name=date)
    showtime_date_name = showtime_date["ShowtimeDate"]
    showtime_movies = showtime_date["Movies"]
    movie_showings = _get_movie_showings(movie_list=showtime_movies, movie_title=movie)
    movie_title = movie_showings["Title"]
    showdate = ShowDate(
        date=showtime_date_name,
        cinemas=[
            Cinema(
                name=cinema_name,
                movies=[
                    Movie(
                        title=movie_title,
                        showtimes=_get_showtimes(movie_showings=movie_showings, format=format),
                    )
                ],
            )
        ],
    )
    return showdate


def _get_formatted_showings_by_cinema(
    date: str,
    cinema_tag: str,
    zone_showings: List[Dict[str, Any]],
    movie: str,
    format: str,
) -> Optional[Cinema]:
    """

    :param date:
    :param cinema_tag:
    :param zone_showings:
    :param movie:
    :param format:
    :return:
    """
    cinema_showing = get_showing_by_cinemas_and_cinema_tag(showings=zone_showings, cinema_tag=cinema_tag)
    if not cinema_showing:
        return None
    showtime_date = _get_showtime_by_date(showing=cinema_showing, date_name=date.replace("-", " "))
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
                    showtimes=_get_showtimes(movie_showings=movie_showing, format=format),
                )
            )
    cinema_showtimes = Cinema(name=cinema_showing["Name"], movies=movies)
    return cinema_showtimes


def _get_formatted_showings_by_zone(
    date: str, zone: str, movie: str, format: str
) -> List[Cinema]:
    """

    :param date:
    :param zone:
    :param movie:
    :param format:
    :return:
    """
    if zone not in CINEMAS:
        return []
    zone_showings = _get_showings_response_by_zone(zone=zone)
    cinemas_in_zone = CINEMAS[zone]
    zone_showtimes = []
    for cinema in cinemas_in_zone["list"]:
        zone_showtime = _get_formatted_showings_by_cinema(
            date=date, cinema_tag=cinema["tag"], zone_showings=zone_showings, movie=movie, format=format
        )
        if not zone_showtime:
            continue
        zone_showtimes.append(zone_showtime)
    return zone_showtimes


def _get_zones(zone_name: str) -> Tuple[List[str], bool]:
    """

    :param zone_name:
    :return:
    """
    is_city = False
    if zone_name == "santiago":
        zones = CINEMAS_SANTIAGO
    elif zone_name in CINEMA_CITIES.keys():
        is_city = True
        zones = [CINEMA_CITIES[zone_name]]
    else:
        zones = [zone_name]
    return zones, is_city


def _get_zone_showings(
    zone: str, zone_name: str, is_city: bool
) -> List[Dict[str, Any]]:
    """

    :param zone:
    :param zone_name:
    :param is_city:
    :return:
    """
    zone_showings = _get_showings_response_by_zone(zone=zone)
    if is_city:
        zone_showings = _get_showings_from_specific_cinemas(
            cinema_showings=zone_showings, cinemas=_get_cinemas_by_zone(zone=zone_name)
        )
    return zone_showings


def get_showings_by_zone(
    movie: str, date: str, zone_name: str, format: str
) -> List[Cinema]:
    """

    :param movie:
    :param date:
    :param zone_name:
    :param format:
    :return:
    """
    zones, is_city = _get_zones(zone_name=zone_name)
    cinema_showtimes = []
    for zone in zones:
        zone_showings = _get_zone_showings(zone=zone, zone_name=zone_name, is_city=is_city)
        for cinema in zone_showings:
            cinema_showtime = _get_formatted_showings_by_cinema(
                date=date, cinema_tag=cinema["Key"], zone_showings=zone_showings, movie=movie, format=format
            )
            if not cinema_showtime:
                continue
            cinema_showtimes.append(cinema_showtime)
    return cinema_showtimes


def get_showing_by_date(movie: str, date: str, format: str) -> List[Cinema]:
    """

    :param movie:
    :param date:
    :param format:
    :return:
    """
    cinema_showtimes = []
    for zone in CINEMAS:
        cinema_showtime = _get_formatted_showings_by_zone(date=date, zone=zone, movie=movie, format=format)
        if not cinema_showtime:
            continue
        cinema_showtimes += cinema_showtime
    return cinema_showtimes


def _get_showdate_from_showtime_date(
    showtime_date: Dict[str, Any], movie: str, cinema_name: str, format: str
) -> Optional[ShowDate]:
    """

    :param showtime_date:
    :param movie:
    :param cinema_name:
    :param format:
    :return:
    """
    showtime_date_name = showtime_date["ShowtimeDate"]
    showtime_movies = showtime_date["Movies"]
    movie_showings = _get_movie_showings(movie_list=showtime_movies, movie_title=movie)
    if not movie_showings:
        return
    movie_title = movie_showings["Title"]
    return ShowDate(
        date=showtime_date_name,
        cinemas=[
            Cinema(
                name=cinema_name,
                movies=[
                    Movie(
                        title=movie_title,
                        showtimes=_get_showtimes(movie_showings=movie_showings, format=format),
                    )
                ],
            )
        ],
    )


def get_showing_by_cinema(
    movie: str, cinema: str, format: str = None
) -> List[ShowDate]:
    """

    :param movie:
    :param cinema:
    :param format:
    :return:
    """
    zone = _get_zone_by_cinema(cinema=cinema)
    cinema_showings = get_showing_by_cinemas_and_cinema_tag(
        showings=_get_showings_response_by_zone(zone=zone), cinema_tag=cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    total_showings = []
    for showtime_date in cinema_dates:
        showdate = _get_showdate_from_showtime_date(
            showtime_date=showtime_date, movie=movie, cinema_name=cinema_name, format=format
        )
        if showdate:
            total_showings.append(showdate)
    return total_showings


def get_showing_by_zone(
    movie: str, zone_name: str, format: str = None
) -> List[ShowDate]:
    """

    :param movie:
    :param zone_name:
    :param format:
    :return:
    """
    zones, is_city = _get_zones(zone_name=zone_name)
    total_showings = []
    for zone in zones:
        zone_showings = _get_zone_showings(zone=zone, zone_name=zone_name, is_city=is_city)
        for cinema_showings in zone_showings:
            cinema_name = cinema_showings["Name"]
            cinema_dates = cinema_showings["Dates"]
            total_showings = []
            for showtime_date in cinema_dates:
                showdate = _get_showdate_from_showtime_date(
                    showtime_date=showtime_date, movie=movie, cinema_name=cinema_name, format=format
                )
                if showdate:
                    total_showings.append(showdate)
    return total_showings


def _get_movie_showtimes(
    showtime_movies: List[Dict[str, Any]], format: str
) -> List[Movie]:
    """

    :param showtime_movies:
    :param format:
    :return:
    """
    movies = []
    for movie_showings in showtime_movies:
        movie_title = movie_showings["Title"]
        movies.append(
            Movie(title=movie_title, showtimes=_get_showtimes(movie_showings=movie_showings, format=format))
        )
    return movies


def get_cinema_showings(cinema: str, format: str) -> List[ShowDate]:
    """

    :param cinema:
    :param format:
    :return:
    """
    zone = _get_zone_by_cinema(cinema=cinema)
    cinema_showings = get_showing_by_cinemas_and_cinema_tag(
        showings=_get_showings_response_by_zone(zone=zone), cinema_tag=cinema
    )
    cinema_name = cinema_showings["Name"]
    cinema_dates = cinema_showings["Dates"]
    total_showings = []
    for showtime_date in cinema_dates:
        showtime_date_name = showtime_date["ShowtimeDate"]
        movies = _get_movie_showtimes(showtime_movies=showtime_date["Movies"], format=format)
        total_showings.append(
            ShowDate(
                date=showtime_date_name,
                cinemas=[Cinema(name=cinema_name, movies=movies)],
            )
        )
    return total_showings


def get_cinema_showings_by_zone(zone_name: str, format: str) -> List[ShowDate]:
    """

    :param zone_name:
    :param format:
    :return:
    """
    zones, is_city = _get_zones(zone_name=zone_name)
    total_showings = []
    for zone in zones:
        zone_showings = _get_zone_showings(zone=zone, zone_name=zone_name, is_city=is_city)
        for cinema_showings in zone_showings:
            cinema_name = cinema_showings["Name"]
            cinema_dates = cinema_showings["Dates"]
            for showtime_date in cinema_dates:
                showtime_date_name = showtime_date["ShowtimeDate"]
                movies = _get_movie_showtimes(showtime_movies=showtime_date["Movies"], format=format)
                total_showings.append(
                    ShowDate(
                        date=showtime_date_name,
                        cinemas=[Cinema(name=cinema_name, movies=movies)],
                    )
                )
    return total_showings


def get_cinema_showings_by_date(cinema: str, date: str, format: str) -> ShowDate:
    """

    :param cinema:
    :param date:
    :param format:
    :return:
    """
    zone = _get_zone_by_cinema(cinema=cinema)
    cinema_showing = get_showing_by_cinemas_and_cinema_tag(
        showings=_get_showings_response_by_zone(zone=zone), cinema_tag=cinema
    )
    cinema_name = cinema_showing["Name"]
    showtime_date = _get_showtime_by_date(showing=cinema_showing, date_name=date.replace("-", " "))
    showtime_date_name = showtime_date["ShowtimeDate"]
    movies = _get_movie_showtimes(showtime_movies=showtime_date["Movies"], format=format)
    return ShowDate(
        date=showtime_date_name, cinemas=([Cinema(name=cinema_name, movies=movies)])
    )


def get_cinema_showings_by_date_and_zone(
    zone_name: str, date: str, format: str
) -> List[ShowDate]:
    """

    :param zone_name:
    :param date:
    :param format:
    :return:
    """
    zones, is_city = _get_zones(zone_name=zone_name)
    total_showings = []
    for zone in zones:
        zone_showings = _get_zone_showings(zone=zone, zone_name=zone_name, is_city=is_city)
        for cinema_showing in zone_showings:
            cinema_name = cinema_showing["Name"]
            showtime_date = _get_showtime_by_date(
                showing=cinema_showing, date_name=date.replace("-", " ")
            )
            showtime_date_name = showtime_date["ShowtimeDate"]
            movies = _get_movie_showtimes(showtime_movies=showtime_date["Movies"], format=format)
            total_showings.append(
                ShowDate(
                    date=showtime_date_name,
                    cinemas=([Cinema(name=cinema_name, movies=movies)]),
                )
            )
    return total_showings


def get_total(date: str, format: str) -> List[Cinema]:
    """

    :param date:
    :param format:
    :return:
    """
    cinema_showtimes = []
    for zone in CINEMAS:
        cinema_showtime = _get_formatted_showings_by_zone(date=date, zone=zone, movie="", format=format)
        if not cinema_showtime:
            continue
        cinema_showtimes += cinema_showtime
    return cinema_showtimes
