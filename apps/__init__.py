from apps.cinehoyts import services as cinehoyts_services
from apps.cinehoyts.constants import CINEMAS
from apps.cinemark import services as cinemark_services


def get_chain(cinema):
    if cinehoyts_services.is_chain(cinema):
        return "CINEHOYTS"
    elif cinemark_services.is_chain(cinema):
        return "CINEMARK"
    return None


def get_showings(movie, date, cinema):
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_showings(movie, date, cinema)
    elif chain == "CINEMARK":
        return cinemark_services.get_showings(movie, date, cinema)


def get_showings_by_zone(movie, date, cinema):
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_showings_by_zone(movie, date, cinema)
    elif chain == "CINEMARK":
        return cinemark_services.get_showings_by_zone(movie, date, cinema)


def get_showing_by_date(movie, date):
    showings = (
        f"CINEHOYTS\n—————\n{cinehoyts_services.get_showing_by_date(movie, date)}"
    )
    showings += f"CINEMARK\n—————\n{cinemark_services.get_showing_by_date(movie, date)}"
    return showings


def get_showing_by_cinema(movie, cinema, format):
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_showing_by_cinema(movie, cinema, format)
    elif chain == "CINEMARK":
        return cinemark_services.get_showing_by_cinema(movie, cinema, format)


def get_cinema_showings_by_date(cinema, date):
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_cinema_showings_by_date(cinema, date)
    elif chain == "CINEMARK":
        return cinemark_services.get_cinema_showings_by_date(cinema, date)


def get_cinema_showings(cinema):
    chain = get_chain(cinema)
    if chain == "CINEHOYTS":
        return cinehoyts_services.get_cinema_showings(cinema)
    elif chain == "CINEMARK":
        return cinemark_services.get_cinema_showings(cinema)


def get_info_cities(zone):
    return cinehoyts_services.get_info_cities(zone)


def get_info_cinemas():
    return cinehoyts_services.get_info_cinemas()
