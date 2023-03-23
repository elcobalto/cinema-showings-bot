import unittest
from parameterized import parameterized

from apps.cinema.services import cinehoyts
from apps.cinema.constants.cinehoyts import CINEMAS
import json

ANTOFAGASTA_CINEMAS = [
    {
        "id": "cinehoyts-espacio-urbano-antofagasta",
        "name": "CineHoyts Espacio Urbano Antofagasta",
        "tag": "cinehoyts-espacio-urbano-antofagasta",
    },
    {
        "id": "mallplaza-antofagasta",
        "name": "MallPlaza Antofagasta",
        "tag": "mallplaza-antofagasta",
    },
]

SANTIAGO_ORIENTE_CINEMAS = [
    {
        "name": "Cinepolis Casa Costanera",
        "tag": "cinepolis-casa-costanera",
        "id": "cinepolis-casa-costanera",
    },
    {
        "name": "Cinepolis La Reina",
        "tag": "cinepolis-la-reina",
        "id": "cinepolis-la-reina",
    },
    {
        "name": "Cinepolis MallPlaza Egaña",
        "tag": "cinepolis-mallplaza-egana",
        "id": "cinepolis-mallplaza-egana",
    },
    {
        "name": "Cinepolis MallPlaza Egaña Premium Class",
        "tag": "cinepolis-mallplaza-egana-premium-class",
        "id": "cinepolis-mallplaza-egana-premium-class",
    },
    {
        "name": "CineHoyts Paseo Los Domínicos (San Carlos)",
        "tag": "paseo-los-dominicos-(san-carlos)",
        "id": "paseo-los-dominicos-(san-carlos)",
    },
    {
        "name": "CineHoyts MallPlaza Los Domínicos",
        "tag": "cinepolis-mallplaza-los-dominicos",
        "id": "cinepolis-mallplaza-los-dominicos",
    },
    {
        "name": "CineHoyts MallPlaza Los Domínicos Premium Class",
        "tag": "cinepolis-mallplaza-los-dominicos-premium-class",
        "id": "cinepolis-mallplaza-los-dominicos-premium-class",
    },
    {
        "name": "Cinepolis Paseo Los Trapenses",
        "tag": "cinepolis-paseo-los-trapenses",
        "id": "cinepolis-paseo-los-trapenses",
    },
    {"name": "CineHoyts Parque Arauco", "tag": "parque-arauco", "id": "parque-arauco"},
    {
        "name": "CineHoyts Parque Arauco Premium Class",
        "tag": "parque-arauco-premium-class",
        "id": "parque-arauco-premium-class",
    },
]

SHOWINGS = json.load(open("apps/cinema/services/tests/cinepolis-la-reina.json"))

SHOWING_DATES = json.load(
    open("apps/cinema/services/tests/cinepolis-la-reina-dates.json")
)

SHOWING_DATES_5_MARZO = json.load(
    open("apps/cinema/services/tests/cinepolis-la-reina-dates-5-marzo.json")
)


class TestCineHoytsServices(unittest.TestCase):
    @parameterized.expand(
        [
            ["", None],
            ["cine-universal", None],
            ["valparaiso", "norte-y-centro-de-chile"],
            ["arauco-estacion", "santiago-centro"],
            ["cinepolis-la-reina", "santiago-oriente"],
            ["arauco-maipu", "santiago-poniente-y-norte"],
            ["mallplaza-sur", "santiago-sur"],
            ["arauco-chillan", "sur-de-chile"],
        ]
    )
    def test_get_zone_by_cinema_tag(self, cinema_tag, zone):
        self.assertEqual(cinehoyts.get_zone_by_cinema_tag(cinema_tag), zone)

    @parameterized.expand(
        [
            ["", CINEMAS.keys()],
            ["cine-universal", CINEMAS.keys()],
            ["valparaiso", ["norte-y-centro-de-chile"]],
            ["arauco-estacion", ["santiago-centro"]],
            ["cinepolis-la-reina", ["santiago-oriente"]],
            ["arauco-maipu", ["santiago-poniente-y-norte"]],
            ["mallplaza-sur", ["santiago-sur"]],
            ["arauco-chillan", ["sur-de-chile"]],
        ]
    )
    def test_get_zones_by_cinema_tag(self, cinema_tag, zones):
        self.assertEqual(cinehoyts.get_zones_by_cinema_tag(cinema_tag), zones)

    @parameterized.expand(
        [
            ["", False],
            ["cine-universal", False],
            ["valparaiso", True],
            ["arauco-estacion", True],
            ["cinepolis-la-reina", True],
            ["arauco-maipu", True],
            ["mallplaza-sur", True],
            ["arauco-chillan", True],
        ]
    )
    def test_is_chain(self, zone_tag, is_chain):
        self.assertEqual(cinehoyts.is_chain(zone_tag), is_chain)

    @parameterized.expand(
        [
            ["", []],
            ["antofagasta", ANTOFAGASTA_CINEMAS],
            ["santiago-oriente", SANTIAGO_ORIENTE_CINEMAS],
        ]
    )
    def test_get_cinemas_by_zone_tag(self, zone_tag, cinemas):
        self.assertEqual(cinehoyts.get_cinemas_by_zone_tag(zone_tag), cinemas)

    @parameterized.expand(
        [
            [SHOWINGS, ANTOFAGASTA_CINEMAS, []],
            [SHOWINGS, SANTIAGO_ORIENTE_CINEMAS, SHOWINGS],
        ]
    )
    def test_get_showings_from_specific_cinemas(
        self, cinema_showings, cinemas, showings
    ):
        self.assertEqual(
            cinehoyts.get_showings_from_specific_cinemas(cinema_showings, cinemas),
            showings,
        )

    @parameterized.expand(
        [
            [SHOWING_DATES, "", SHOWING_DATES["Dates"]],
            [SHOWING_DATES, "5-marzo", [SHOWING_DATES_5_MARZO]],
        ]
    )
    def test_get_showtime_by_date(self, showing, date_name, showtime):
        self.assertEqual(
            cinehoyts.get_showtime_by_date(showing, date_name),
            showtime,
        )
