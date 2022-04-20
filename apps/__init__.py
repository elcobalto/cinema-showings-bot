from typing import List, Optional, Tuple

from apps.cinema.dataclasses import Cinema, ShowDate
from apps.cinema.services import cinehoyts as cinehoyts_services
from apps.cinema.services import cinemark as cinemark_services
from apps.constants import CINEMAS_ZONES
from apps.movie.dataclasses import Movie, ShowTime


def get_chain(cinema: str) -> Optional[str]:
    if cinehoyts_services.is_chain(cinema):
        return "CINEHOYTS"
    elif cinemark_services.is_chain(cinema):
        return "CINEMARK"
    return None


def get_showings(movie, date, cinema) -> ShowDate:
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_showings(movie, date, cinema)
    elif chain == "CINEMARK":
        return cinemark_services.get_showings(movie, date, cinema)


def get_showings_by_zone(movie, date, cinema) -> ShowDate:
    cinehoyts_cinemas = cinehoyts_services.get_showings_by_zone(movie, date, cinema)
    cinemark_cinemas = cinemark_services.get_showings_by_zone(movie, date, cinema)
    return ShowDate(date=date, cinemas=cinehoyts_cinemas + cinemark_cinemas)


def get_showing_by_date(movie, date) -> ShowDate:
    cinehoyts_cinemas = cinehoyts_services.get_showing_by_date(movie, date)
    cinemark_cinemas = cinemark_services.get_showing_by_date(movie, date)
    return ShowDate(date=date, cinemas=cinehoyts_cinemas + cinemark_cinemas)


def get_general_showings(movie: str, date: str, cinema: str = None) -> Tuple[str, int]:
    cinema_is_zone = cinema in CINEMAS_ZONES
    if cinema and not cinema_is_zone:
        cinema_showings = get_showings(movie, date, cinema)
        message, total = get_movie_date_message([cinema_showings], "CINEMA")
    elif cinema and cinema_is_zone:
        cinema_showings = get_showings_by_zone(movie, date, cinema)
        message, total = get_movie_date_message([cinema_showings], "CINEMA")
    else:
        cinema_showings = get_showing_by_date(movie, date)
        message, total = get_movie_date_message([cinema_showings], "CINEMA")
    return message, total


def get_showing_by_cinema(movie, cinema, format) -> List[ShowDate]:
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_showing_by_cinema(movie, cinema, format)
    elif chain == "CINEMARK":
        return cinemark_services.get_showing_by_cinema(movie, cinema, format)


def get_cinema_showings_by_date(cinema, date) -> ShowDate:
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_cinema_showings_by_date(cinema, date)
    elif chain == "CINEMARK":
        return cinemark_services.get_cinema_showings_by_date(cinema, date)


def get_cinema_showings(cinema) -> List[ShowDate]:
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_cinema_showings(cinema)
    elif chain == "CINEMARK":
        return cinemark_services.get_cinema_showings(cinema)


def get_general_cinema_showings(cinema: str, date: str = None) -> Tuple[str, int]:
    if date:
        cinema_showings = get_cinema_showings_by_date(cinema, date)
        message, total = get_movie_date_message([cinema_showings], "CINEMA")
    else:
        cinema_showings = get_cinema_showings(cinema)
        message, total = get_movie_date_message(cinema_showings, "CINEMA")
    return message, total


def get_movie_date_message(
    showdates: List[ShowDate], separator_type: str
) -> Tuple[str, int]:
    result = ""
    total_shotimes = 0
    for showdate in showdates:
        if not showdate:
            continue
        temp_result = f"{showdate.get_formatted_date()}\n\n"
        is_there_any_cinema = False
        for cinema in showdate.cinemas:
            movie_temp_result = f"{cinema.name}\n\n"
            is_there_any_movie = False
            for movie in cinema.movies:
                show_temp_result = f"{movie.get_formatted_title()}\n"
                is_there_showtime = False
                for showtime in movie.showtimes:
                    is_there_any_cinema = True
                    is_there_any_movie = True
                    is_there_showtime = True
                    show_temp_result += f"{showtime.showtime} hrs — {showtime.format}\n"
                    total_shotimes += 1
                show_temp_result += "——————\n\n"
                if separator_type == "MOVIE":
                    show_temp_result += "\n\n$SEPARATOR$"
                if is_there_showtime:
                    movie_temp_result += show_temp_result
            if separator_type == "CINEMA":
                movie_temp_result += "$SEPARATOR$"
            if is_there_any_movie:
                temp_result += movie_temp_result
        if is_there_any_cinema:
            result += temp_result
        if separator_type == "SHOWTIME":
            result += "\n\n$SEPARATOR$"
    return result, total_shotimes


def get_info_cities():
    return cinehoyts_services.get_info_cities() + cinemark_services.get_info_cities()


def get_info_cinemas():
    return cinehoyts_services.get_info_cinemas() + cinemark_services.get_info_cinemas()
