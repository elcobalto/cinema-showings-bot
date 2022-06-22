from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple

from apps.cinema.dataclasses import Cinema, ShowDate
from apps.cinema.services import cinehoyts as cinehoyts_services
from apps.cinema.services import cinemark as cinemark_services
from apps.discord.constants import CINEMAS, CINEMAS_ZONES


def get_chain(cinema: str) -> Optional[str]:
    """

    :param cinema:
    :return:
    """
    if cinehoyts_services.is_chain(cinema_tag=cinema):
        return "CINEHOYTS"
    elif cinemark_services.is_chain(cinema=cinema):
        return "CINEMARK"
    return None


def get_showings(movie: str, date: str, cinema: str, format: str) -> List[ShowDate]:
    """

    :param movie:
    :param date:
    :param cinema:
    :param format:
    :return:
    """
    chain = get_chain(cinema=cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_showings(
            movie_tag=movie, date=date, cinema_tag=cinema, show_format=format
        )
    elif chain == "CINEMARK":
        return cinemark_services.get_showings(
            movie_tag=movie, date=date, cinema_tag=cinema, format=format
        )


def get_showings_by_zone(movie: str, date: str, zone: str, format: str) -> ShowDate:
    """

    :param movie:
    :param date:
    :param zone:
    :param format:
    :return:
    """
    cinehoyts_cinemas = cinehoyts_services.get_cinemas_showings_by_zone(
        movie_tag=movie, date=date, zone_name=zone, show_format=format
    )
    cinemark_cinemas = cinemark_services.get_showings_by_zone(
        movie=movie, date=date, zone_name=zone, format=format
    )
    return ShowDate(date=date, cinemas=cinehoyts_cinemas + cinemark_cinemas)


def get_general_showings(
    movie: str, date: str, cinema: str = None, format: str = None
) -> Tuple[str, int]:
    """

    :param movie:
    :param date:
    :param cinema:
    :param format:
    :return:
    """
    cinema_is_zone = cinema in CINEMAS_ZONES
    if not cinema_is_zone:
        cinema_showings = get_showings(
            movie=movie, date=date, cinema=cinema, format=format
        )
        message, total = get_movie_date_message(
            showdates=cinema_showings, separator_type="CINEMA"
        )
    else:
        cinema_showings = get_showings_by_zone(
            movie=movie, date=date, zone=cinema, format=format
        )
        message, total = get_movie_date_message(
            showdates=cinema_showings, separator_type="CINEMA"
        )
    return message, total


def get_movie_date_message(
    showdates: List[ShowDate], separator_type: str
) -> Tuple[str, int]:
    """

    :param showdates:
    :param separator_type:
    :return:
    """
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
                    if showtime.seats:
                        seats = (
                            f"{showtime.seats} asientos disponibles"
                            if int(showtime.seats) > 0
                            else "AGOTADA"
                        )
                        show_temp_result += (
                            f"{showtime.showtime} hrs — {showtime.format} — {seats}\n"
                        )
                    else:
                        show_temp_result += (
                            f"{showtime.showtime} hrs — {showtime.format}\n"
                        )
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


def similar(a: str, b: str) -> float:
    """

    :param a:
    :param b:
    :return:
    """
    return SequenceMatcher(None, a, b).ratio()


def _check_movie_in_total(movie_title: str, total: Dict[str, Any]):
    """

    :param movie_title:
    :param total:
    :return:
    """
    for possible_movie in total.keys():
        similarity = similar(a=movie_title, b=possible_movie)
        if (
            (movie_title in possible_movie)
            or (possible_movie in movie_title)
            or similarity > 0.6
        ):
            return True, possible_movie
    return False, movie_title


def _get_movie_total(cinemas: List[Cinema]) -> str:
    """

    :param cinemas:
    :return:
    """
    total = {}
    for cinema in cinemas:
        for movie in cinema.movies:
            movie_title = movie.title.upper().replace("-", " ").replace(":", "")
            movie_exists, movie_key = _check_movie_in_total(
                movie_title=movie_title, total=total
            )
            if movie_exists:
                total[movie_key] += len(movie.showtimes)
            else:
                total[movie_key] = len(movie.showtimes)
    total = {
        k: v for k, v in sorted(total.items(), key=lambda item: item[1], reverse=True)
    }
    message = ""
    for movie_title in total.keys():
        message += f"{movie_title}: {total[movie_title]}\n"
    return message


def _get_format_total(cinemas: List[Cinema]) -> str:
    """

    :param cinemas:
    :return:
    """
    total = {}
    for cinema in cinemas:
        for movie in cinema.movies:
            for showtime in movie.showtimes:
                showtime_format = showtime.format
                if showtime_format in total:
                    total[showtime_format] += 1
                else:
                    total[showtime_format] = 1
    total = {
        k: v for k, v in sorted(total.items(), key=lambda item: item[1], reverse=True)
    }
    message = ""
    for showtime_format in total.keys():
        message += f"{showtime_format}: {total[showtime_format]}\n"
    return message


def _get_cinema_total(cinemas: List[Cinema]) -> str:
    """

    :param cinemas:
    :return:
    """
    total = {}
    for cinema in cinemas:
        for movie in cinema.movies:
            if cinema.name in total:
                total[cinema.name] += len(movie.showtimes)
            else:
                total[cinema.name] = len(movie.showtimes)
    total = {
        k: v for k, v in sorted(total.items(), key=lambda item: item[1], reverse=True)
    }
    message = ""
    for cinema_name in total.keys():
        message += f"{cinema_name}: {total[cinema_name]}\n"
    return message


def get_total(date: str, format: str) -> str:
    """

    :param date:
    :param format:
    :return:
    """
    cinehoyts_total = cinehoyts_services.get_total(date=date, format=format)
    cinemark_total = cinemark_services.get_total(date=date, format=format)
    total = _get_movie_total(cinemas=cinehoyts_total + cinemark_total)
    return total


def get_format_total(date: str, format: str) -> str:
    """

    :param date:
    :param format:
    :return:
    """
    cinehoyts_total = cinehoyts_services.get_total(date, format)
    cinemark_total = cinemark_services.get_total(date, format)
    total = _get_format_total(cinemas=cinehoyts_total + cinemark_total)
    return total


def get_cinema_total(date: str, format: str) -> str:
    """

    :param date:
    :param format:
    :return:
    """
    cinehoyts_total = cinehoyts_services.get_total(date, format)
    cinemark_total = cinemark_services.get_total(date, format)
    total = _get_cinema_total(cinemas=cinehoyts_total + cinemark_total)
    return total


def get_info_cities():
    """

    :return:
    """
    info = ""
    uniques = {}
    CINEMAS_ZONES.sort()
    for cinema in CINEMAS_ZONES:
        if cinema in uniques:
            continue
        info += f"{cinema}\n"
        uniques[cinema] = True
    return info


def get_info_cinemas():
    """

    :return:
    """
    info = ""
    uniques = {}
    CINEMAS.sort()
    for cinema in CINEMAS:
        if cinema in uniques:
            continue
        info += f"{cinema}\n"
        uniques[cinema] = True
    return info
