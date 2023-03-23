from typing import Any, Dict, List, Optional, Tuple

import requests
import ipdb

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


def get_zone_by_cinema_tag(cinema_tag: str) -> Optional[str]:
    """
    Gets a zone tag from a cinema tag. Returns None for a not mapped zone tag.
    :param cinema_tag: cinema tag.
    :return: Zone tag.
    """
    if cinema_tag in NORTE_Y_CENTRO_DE_CHILE_TAGS:
        return "norte-y-centro-de-chile"
    elif cinema_tag in SANTIAGO_CENTRO_TAGS:
        return "santiago-centro"
    elif cinema_tag in SANTIAGO_ORIENTE_TAGS:
        return "santiago-oriente"
    elif cinema_tag in SANTIAGO_NORTE_Y_PONIENTE_TAGS:
        return "santiago-poniente-y-norte"
    elif cinema_tag in SANTIAGO_SUR_TAGS:
        return "santiago-sur"
    elif cinema_tag in SUR_DE_CHILE_TAGS:
        return "sur-de-chile"
    return None


def get_zones_by_cinema_tag(cinema_tag: str) -> List[str]:
    """
    Gets a zone tag from a cinema tag. Returns None for a not mapped zone tag.
    :param cinema_tag: cinema tag.
    :return: Zone tag.
    """
    zone = get_zone_by_cinema_tag(cinema_tag=cinema_tag)
    if zone:
        return [zone]
    return CINEMAS.keys()


def is_chain(cinema_tag: str) -> bool:
    """
    Determines if a cinema belongs to the CineHoyts chain.
    :param cinema_tag: Cinema tag.
    :return: Descriptor if a cinema is from CineHoyts.
    """
    zone = get_zone_by_cinema_tag(cinema_tag=cinema_tag)
    return zone is not None


def get_showings_response_by_zone_tag(
    zone_tag: str = "santiago-oriente",
) -> List[Dict[str, Any]]:
    """
    Gets showings response from a zone tag.
    :param zone_tag: Zone tag.
    :return: Showings response.
    """
    try:
        payload = {"claveCiudad": zone_tag, "esVIP": True}
        showings = requests.post(
            f"{CINEHOYTS_HOST}/Cartelera.aspx/GetNowPlayingByCity", json=payload
        )
        clean_showings = showings.json()
        return clean_showings["d"]["Cinemas"]
    except Exception:
        return []


def get_cinemas_by_zone_tag(zone_tag: str) -> List[Dict[str, Any]]:
    """
    Gets a cinema dataclass list from a general zone name.
    :param zone_name: Zone name.
    :return: List of cinema dataclasses.
    """
    for cinema_zone in CINEMA_ZONES:
        if cinema_zone["tag"] == zone_tag:
            return cinema_zone["list"]
    return []


def get_showings_from_specific_cinemas(
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


def get_showtime_by_date(
    showing: Dict[str, Any], date_name: str
) -> List[Dict[str, Any]]:
    """
    Gets cinema showtimes by an specific date.
    :param showing: Cinema with showtimes.
    :param date_name: Date to be searched.
    :return: Cinema showtime.
    """
    if not date_name:
        return showing["Dates"]
    for showtime_date in showing["Dates"]:
        formatted_showtime_date = showtime_date["ShowtimeDate"].replace(" ", "-")
        day, month = formatted_showtime_date.split("-")
        if int(day) < 10 and len(day) == 2:
            formatted_showtime_date = formatted_showtime_date[1:]
        formatted_searched_date = date_name.replace(" ", "-")
        if formatted_showtime_date == formatted_searched_date:
            return [showtime_date]
    return {}


def _check_date(date: str, showtime_date: Dict[str, Any]) -> bool:
    """

    :param showtime_date:
    :param date:
    :return:
    """
    if not date:
        return True
    formatted_showtime_date = showtime_date["ShowtimeDate"].replace(" ", "-")
    day, month = formatted_showtime_date.split("-")
    if int(day) < 10 and len(day) == 2:
        formatted_showtime_date = formatted_showtime_date[1:]
    formatted_searched_date = date.replace(" ", "-")
    return formatted_showtime_date == formatted_searched_date


def _get_movie_showings(movie_list: List[Dict[str, Any]], movie_tag: str) -> Dict:
    """
    Gets movie showings from list of movies with a to be searched movie title.
    :param movie_list: List of movie showings.
    :param movie_tag: Movie title.
    :return: Movie showings.
    """
    for movie in movie_list:
        if movie_tag in movie["Key"] or movie["Key"] in movie_tag:
            return movie
    return {}


def _get_formatted_show_format(show_format: str):
    """
    Formats a showtime format.
    :param show_format: Showtime format.
    :return: Formatted showtime format.
    """
    if show_format == "ESP":
        return "2D ESP"
    if show_format == "SUBT":
        return "2D SUB"
    show_format = show_format.replace("DOB", "ESP")
    show_format = show_format.replace("SUBT", "SUB")
    return show_format


def _get_showtimes(movie_showings: Dict, show_format: str = None) -> List[ShowTime]:
    """
    Gets list of showtimes dataclasses objects from movie showings. Filtered by format if given.
    :param movie_showings: Movie showings.
    :param show_format: Optional showtime format.
    :return: List of showtimes dataclasses objects.
    """
    total_showtimes = []
    for formats in movie_showings["Formats"]:
        showtimes = formats["Showtimes"]
        format_name = _get_formatted_show_format(show_format=formats["Name"])
        if show_format and show_format not in format_name:
            continue
        for show in showtimes:
            showtime = show["Time"]
            total_showtimes.append(
                ShowTime(showtime=showtime, format=format_name, seats="")
            )
    return total_showtimes


def get_showings(
    movie_tag: str, date: str, cinema_tag: str, show_format: str
) -> List[ShowDate]:
    """
    Gets showings from an specific movie, date, cinema and show_format.
    :param movie_tag: Movie title
    :param date: Date.
    :param cinema_tag: Cinema tag.
    :param show_format: Format of the showtime.
    :return: Showdate searched if found.
    """
    zones = get_zones_by_cinema_tag(cinema_tag=cinema_tag)
    total: Dict[str, Dict[str, List[Movie]]] = {}
    for zone in zones:
        showings = get_showings_response_by_zone_tag(zone_tag=zone)
        for cinema_showing in showings:
            if not cinema_showing["Key"] == cinema_tag:
                continue
            cinema_name = cinema_showing["Name"]
            for showtime_date in cinema_showing["Dates"]:
                is_date = _check_date(date=date, showtime_date=showtime_date)
                if not is_date:
                    continue
                showtime_date_name = showtime_date["ShowtimeDate"]
                showtime_movies = showtime_date["Movies"]
                movies = []
                for movie in showtime_movies:
                    if movie_tag and not (
                        movie_tag in movie["Key"] or movie["Key"] in movie_tag
                    ):
                        continue
                    movie_showings = _get_movie_showings(
                        movie_list=showtime_movies, movie_tag=movie_tag
                    )
                    movie_title = movie_showings["Title"]
                    showtimes = _get_showtimes(
                        movie_showings=movie_showings, show_format=show_format
                    )
                    movies.append(Movie(title=movie_title, showtimes=showtimes))
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
    print(showdates)
    return showdates


def _get_formatted_cinema_showings_by_cinema_tag(
    zone_showings: List[Dict[str, Any]],
    movie_tag: str,
    date: str,
    cinema_tag: str,
    show_format: str,
) -> Optional[Cinema]:
    """
    Gets the showings from a cinema, formatted into a Cinema dataclass.
    :param date: Date to be searched.
    :param cinema_tag: Cinema tag name.
    :param zone_showings: Showings of the zone.
    :param movie_tag: Movie title
    :param show_format: Showtime format.
    :return: Cinema with showings if found.
    """
    cinema_showing = get_showing_by_cinemas_and_cinema_tag(
        showings=zone_showings, cinema_tag=cinema_tag
    )
    if not cinema_showing:
        return None
    date = date.replace("-", " ") if date else ""
    showtime_dates = get_showtime_by_date(showing=cinema_showing, date_name=date)
    movies = []
    for showtime_date in showtime_dates:
        if not showtime_date:
            return None
        for movie_showing in showtime_date["Movies"]:
            if not movie_tag or (
                movie_tag in movie_showing["Key"] or movie_showing["Key"] in movie_tag
            ):
                movies.append(
                    Movie(
                        title=movie_showing["Title"],
                        showtimes=_get_showtimes(
                            movie_showings=movie_showing, show_format=show_format
                        ),
                    )
                )
    cinema_showtimes = Cinema(name=cinema_showing["Name"], movies=movies)
    return cinema_showtimes


def _get_formatted_cinemas_showings_by_zone_tag(
    movie_tag: str, date: str, zone_tag: str, show_format: str
) -> List[Cinema]:
    """
    Gets the showings from a zone, formatted into a list of Cinema dataclasses.
    :param date: Date
    :param zone_tag: Zone tag name.
    :param movie_tag: Movie title.
    :param show_format: Format of the show.
    :return: List of found cinemas with showings.
    """
    if zone_tag not in CINEMAS:
        return []
    zone_showings = get_showings_response_by_zone_tag(zone_tag=zone_tag)
    cinemas_in_zone = CINEMAS[zone_tag]
    zone_showtimes = []
    for cinema in cinemas_in_zone["list"]:
        zone_showtime = _get_formatted_cinema_showings_by_cinema_tag(
            zone_showings=zone_showings,
            movie_tag=movie_tag,
            date=date,
            cinema_tag=cinema["tag"],
            show_format=show_format,
        )
        if not zone_showtime:
            continue
        zone_showtimes.append(zone_showtime)
    return zone_showtimes


def _get_zones_tags(zone_name: str) -> Tuple[List[str], bool]:
    """
    Gets mapped zones by zone_tags.
    :param zone_name: Zone name.
    :return: List of related zone tags.
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
    zone_tag: str, zone_name: str, is_city: bool
) -> List[Dict[str, Any]]:
    """
    Gets zone showings from zone tag, zone names and the fact if a zone name refers to a city.
    :param zone_tag: Zone tag.
    :param zone_name: Zone specific name.
    :param is_city: If a zone name refers to a city.
    :return: List of zone showings.
    """
    zone_showings = get_showings_response_by_zone_tag(zone_tag=zone_tag)
    if is_city:
        zone_showings = get_showings_from_specific_cinemas(
            cinema_showings=zone_showings,
            cinemas=get_cinemas_by_zone_tag(zone_tag=zone_name),
        )
    return zone_showings


def get_cinemas_showings_by_zone(
    movie_tag: str, date: str, zone_name: str, show_format: str
) -> List[ShowDate]:
    """
    Gets showings for a movie, date and format, filtered by zone.
    :param movie_tag: Movie title.
    :param date: Date.
    :param zone_name: Zone specific name.
    :param show_format: Show format.
    :return: List of filtered cinema showings.
    """
    zones, is_city = _get_zones_tags(zone_name=zone_name)
    cinema_showtimes = []
    for zone in zones:
        zone_showings = _get_zone_showings(
            zone_tag=zone, zone_name=zone_name, is_city=is_city
        )
        for cinema in zone_showings:
            cinema_showtime = _get_formatted_cinema_showings_by_cinema_tag(
                zone_showings=zone_showings,
                movie_tag=movie_tag,
                date=date,
                cinema_tag=cinema["Key"],
                show_format=show_format,
            )
            if not cinema_showtime:
                continue
            cinema_showtimes.append(cinema_showtime)
    return cinema_showtimes


def _get_showdate_by_showtime_date(
    movie_tag: str, showtime_date: Dict[str, Any], cinema_name: str, show_format: str
) -> Optional[ShowDate]:
    """
    Gets a showdate by movie title, cinema and format, filtered by showtime date.
    :param showtime_date: Showtime date.
    :param movie_tag: Movie title.
    :param cinema_name: Cinema name.
    :param show_format: Format of show.
    :return: Showing showdate dataclass.
    """
    showtime_date_name = showtime_date["ShowtimeDate"]
    showtime_movies = showtime_date["Movies"]
    movie_showings = _get_movie_showings(
        movie_list=showtime_movies, movie_tag=movie_tag
    )
    if not movie_showings:
        return
    movie_title = movie_showings["Title"]
    movies = Movie(
        title=movie_title,
        showtimes=_get_showtimes(
            movie_showings=movie_showings, show_format=show_format
        ),
    )
    cinema = Cinema(name=cinema_name, movies=[movies])
    return ShowDate(date=showtime_date_name, cinemas=[cinema])


def _get_movie_showtimes(
    showtime_movies: List[Dict[str, Any]], show_format: str
) -> List[Movie]:
    """
    Gets a formatted list of movie showings.
    :param showtime_movies: Movies showtime data.
    :param show_format: Format of show.
    :return: List of movie showtimes.
    """
    movies = []
    for movie_showings in showtime_movies:
        movie_title = movie_showings["Title"]
        movies.append(
            Movie(
                title=movie_title,
                showtimes=_get_showtimes(
                    movie_showings=movie_showings, show_format=show_format
                ),
            )
        )
    return movies


def get_cinema_showings_by_zone(zone_name: str, format: str) -> List[ShowDate]:
    """
    Gets a list of show dates from a zone name and format.
    :param zone_name: Zone name.
    :param format: Format of showing.
    :return: List of showings.
    """
    zones, is_city = _get_zones_tags(zone_name=zone_name)
    total_showings = []
    for zone in zones:
        zone_showings = _get_zone_showings(
            zone_tag=zone, zone_name=zone_name, is_city=is_city
        )
        for cinema_showings in zone_showings:
            cinema_name = cinema_showings["Name"]
            cinema_dates = cinema_showings["Dates"]
            for showtime_date in cinema_dates:
                showtime_date_name = showtime_date["ShowtimeDate"]
                movies = _get_movie_showtimes(
                    showtime_movies=showtime_date["Movies"], show_format=format
                )
                total_showings.append(
                    ShowDate(
                        date=showtime_date_name,
                        cinemas=[Cinema(name=cinema_name, movies=movies)],
                    )
                )
    return total_showings


def get_total(date: str, format: str) -> List[Cinema]:
    """
    Gets total list of movie showings for an specific date.
    :param date: Date of showings.
    :param format: Format of showings.
    :return:
    """
    cinema_showtimes = []
    for zone in CINEMAS:
        cinema_showtime = _get_formatted_cinemas_showings_by_zone_tag(
            movie_tag="", date=date, zone_tag=zone, show_format=format
        )
        if not cinema_showtime:
            continue
        cinema_showtimes += cinema_showtime
    return cinema_showtimes
