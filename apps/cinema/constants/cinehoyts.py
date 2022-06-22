ESPACIO_URBANO_ANTOFAGASTA = {
    "name": "CineHoyts Espacio Urbano Antofagasta",
    "tag": "cinehoyts-espacio-urbano-antofagasta",
    "id": "cinehoyts-espacio-urbano-antofagasta",
}
MALLPLAZA_ANTOFAGASTA = {
    "name": "MallPlaza Antofagasta",
    "tag": "mallplaza-antofagasta",
    "id": "mallplaza-antofagasta",
}
ANTOFAGASTA = {
    "tag": "antofagasta",
    "list": [ESPACIO_URBANO_ANTOFAGASTA, MALLPLAZA_ANTOFAGASTA],
}

MALL_PLAZA_CALAMA = {
    "name": "CineHoyts MallPlaza Calama",
    "tag": "mallplaza-calama",
    "id": "mallplaza-calama",
}
CALAMA = {"tag": "calama", "list": [MALL_PLAZA_CALAMA]}

VIVO_COQUIMBO = {
    "name": "CineHoyts Vivo Coquimbo",
    "tag": "cinepolis-vivo-coquimbo",
    "id": "cinepolis-vivo-coquimbo",
}
COQUIMBO = {"tag": "coquimbo", "list": [VIVO_COQUIMBO]}

CINEPOLIS_OVALLE = {
    "name": "Cinepolis Ovalle",
    "tag": "cinepolis-ovalle",
    "id": "cinepolis-ovalle",
}
OVALLE = {"tag": "ovalle", "list": [CINEPOLIS_OVALLE]}

SHOPPING_QUILLOTA = {
    "name": "CineHoyts Shopping Quillota",
    "tag": "cinepolis-shopping-quillota",
    "id": "cinepolis-shopping-quillota",
}
QUILLOTA = {"tag": "ovalle", "list": [SHOPPING_QUILLOTA]}

CINEHOYTS_VALPARAISO = {
    "name": "CineHoyts Valparaiso",
    "tag": "valparaiso",
    "id": "valparaiso",
}
VALPARAISO = {"tag": "valparaiso", "list": [CINEHOYTS_VALPARAISO]}

NORTE_Y_CENTRO_DE_CHILE = {
    "tag": "norte-y-centro-de-chile",
    "list": [
        ESPACIO_URBANO_ANTOFAGASTA,
        MALLPLAZA_ANTOFAGASTA,
        MALL_PLAZA_CALAMA,
        VIVO_COQUIMBO,
        CINEPOLIS_OVALLE,
        SHOPPING_QUILLOTA,
        CINEHOYTS_VALPARAISO,
    ],
}
NORTE_Y_CENTRO_DE_CHILE_TAGS = [city["tag"] for city in NORTE_Y_CENTRO_DE_CHILE["list"]]


ARAUCO_ESTACION = {
    "name": "CineHoyts Arauco Estación",
    "tag": "arauco-estacion",
    "id": "arauco-estacion",
}
VIVO_IMPERIO = {
    "name": "CineHoyts Vivo Imperio",
    "tag": "cinepolis-vivo-imperio",
    "id": "cinepolis-vivo-imperio",
}
SANTIAGO_CENTRO = {"tag": "santiago-centro", "list": [ARAUCO_ESTACION, VIVO_IMPERIO]}
SANTIAGO_CENTRO_TAGS = [city["tag"] for city in SANTIAGO_CENTRO["list"]]

CASA_COSTANERA = {
    "name": "Cinepolis Casa Costanera",
    "tag": "cinepolis-casa-costanera",
    "id": "cinepolis-casa-costanera",
}
LA_REINA = {
    "name": "Cinepolis La Reina",
    "tag": "cinepolis-la-reina",
    "id": "cinepolis-la-reina",
}
MALLPLAZA_EGANA = {
    "name": "Cinepolis MallPlaza Egaña",
    "tag": "cinepolis-mallplaza-egana",
    "id": "cinepolis-mallplaza-egana",
}
MALLPLAZA_EGANA_PREMIUM_CLASS = {
    "name": "Cinepolis MallPlaza Egaña Premium Class",
    "tag": "cinepolis-mallplaza-egana-premium-class",
    "id": "cinepolis-mallplaza-egana-premium-class",
}
PASEO_LOS_DOMINICOS = {
    "name": "CineHoyts Paseo Los Domínicos (San Carlos)",
    "tag": "paseo-los-dominicos-(san-carlos)",
    "id": "paseo-los-dominicos-(san-carlos)",
}
MALLPLAZA_LOS_DOMINICOS = {
    "name": "CineHoyts MallPlaza Los Domínicos",
    "tag": "cinepolis-mallplaza-los-dominicos",
    "id": "cinepolis-mallplaza-los-dominicos",
}
MALLPLAZA_LOS_DOMINICOS_PREMIUM_CLASS = {
    "name": "CineHoyts MallPlaza Los Domínicos Premium Class",
    "tag": "cinepolis-mallplaza-los-dominicos-premium-class",
    "id": "cinepolis-mallplaza-los-dominicos-premium-class",
}
CINEPOLIS_PASEO_LOS_TRAPENSES = {
    "name": "Cinepolis Paseo Los Trapenses",
    "tag": "cinepolis-paseo-los-trapenses",
    "id": "cinepolis-paseo-los-trapenses",
}
PARQUE_ARAUCO = {
    "name": "CineHoyts Parque Arauco",
    "tag": "parque-arauco",
    "id": "parque-arauco",
}
PARQUE_ARAUCO_PREMIUM_CLASS = {
    "name": "CineHoyts Parque Arauco Premium Class",
    "tag": "parque-arauco-premium-class",
    "id": "parque-arauco-premium-class",
}
SANTIAGO_ORIENTE = {
    "tag": "santiago-oriente",
    "list": [
        CASA_COSTANERA,
        LA_REINA,
        MALLPLAZA_EGANA,
        MALLPLAZA_EGANA_PREMIUM_CLASS,
        PASEO_LOS_DOMINICOS,
        MALLPLAZA_LOS_DOMINICOS,
        MALLPLAZA_LOS_DOMINICOS_PREMIUM_CLASS,
        CINEPOLIS_PASEO_LOS_TRAPENSES,
        PARQUE_ARAUCO,
        PARQUE_ARAUCO_PREMIUM_CLASS,
    ],
}
SANTIAGO_ORIENTE_TAGS = [city["tag"] for city in SANTIAGO_ORIENTE["list"]]

ARAUCO_MAIPU = {
    "name": "CineHoyts Arauco Maipú",
    "tag": "arauco-maipu",
    "id": "arauco-maipu",
}
ARAUCO_QUILICURA = {
    "name": "CineHoyts Arauco Quilicura",
    "tag": "arauco-quilicura",
    "id": "arauco-quilicura",
}
PATIO_OUTLET_MAIPU = {
    "name": "Cinepolis Patio Outlet Maipú",
    "tag": "cinepolis-patio-outlet-maipu",
    "id": "cinepolis-patio-outlet-maipu",
}
ESPACIO_URBANO_MELIPILLA = {
    "name": "CineHoyts Espacio Urbano Melipilla",
    "tag": "espacio-urbano-melipilla",
    "id": "espacio-urbano-melipilla",
}
SANTIAGO_NORTE_Y_PONIENTE = {
    "tag": "santiago-poniente",
    "list": [
        ARAUCO_MAIPU,
        ARAUCO_QUILICURA,
        PATIO_OUTLET_MAIPU,
        ESPACIO_URBANO_MELIPILLA,
    ],
}
SANTIAGO_NORTE_Y_PONIENTE_TAGS = [
    city["tag"] for city in SANTIAGO_NORTE_Y_PONIENTE["list"]
]


ESPACIO_URBANO_PUENTE_ALTO = {
    "name": "Cinepolis Espacio Urbano Puente Alto",
    "tag": "cinepolis-espacio-urbano-puente-alto",
    "id": "cinepolis-espacio-urbano-puente-alto",
}
PLAZUELA_INDEPENDENCIA_PUENTE_ALTO = {
    "name": "Cinepolis Plazuela Independencia Puente Alto",
    "tag": "cinepolis-plazuela-independencia-puente-alto",
    "id": "cinepolis-plazuela-independencia-puente-alto",
}
PATIO_OUTLET_LA_FLORIDA = {
    "name": "Cinepolis Patio Outlet La Florida",
    "tag": "cinepolis-patio-outlet-la-florida",
    "id": "cinepolis-patio-outlet-la-florida",
}
MALLPLAZA_SUR = {
    "name": "CineHoyts MallPlaza Sur",
    "tag": "mallplaza-sur",
    "id": "mallplaza-sur",
}
PASEO_SAN_BERNARDO = {
    "name": "CineHoyts Paseo San Bernardo",
    "tag": "paseo-san-bernardo",
    "id": "paseo-san-bernardo",
}
SANTIAGO_SUR = {
    "tag": "santiago-sur",
    "list": [
        ESPACIO_URBANO_PUENTE_ALTO,
        PLAZUELA_INDEPENDENCIA_PUENTE_ALTO,
        PATIO_OUTLET_LA_FLORIDA,
        MALLPLAZA_SUR,
        PASEO_SAN_BERNARDO,
    ],
}
SANTIAGO_SUR_TAGS = [city["tag"] for city in SANTIAGO_SUR["list"]]
SANTIAGO = {
    "tag": "santiago",
    "list": [
        ARAUCO_ESTACION,
        VIVO_IMPERIO,
        CASA_COSTANERA,
        LA_REINA,
        MALLPLAZA_EGANA,
        MALLPLAZA_EGANA_PREMIUM_CLASS,
        PASEO_LOS_DOMINICOS,
        MALLPLAZA_LOS_DOMINICOS,
        MALLPLAZA_LOS_DOMINICOS_PREMIUM_CLASS,
        CINEPOLIS_PASEO_LOS_TRAPENSES,
        PARQUE_ARAUCO,
        PARQUE_ARAUCO_PREMIUM_CLASS,
        ARAUCO_MAIPU,
        ARAUCO_QUILICURA,
        PATIO_OUTLET_MAIPU,
        ESPACIO_URBANO_MELIPILLA,
        ESPACIO_URBANO_PUENTE_ALTO,
        PLAZUELA_INDEPENDENCIA_PUENTE_ALTO,
        PATIO_OUTLET_LA_FLORIDA,
        MALLPLAZA_SUR,
        PASEO_SAN_BERNARDO,
    ],
}

VIVO_SAN_FERNARDO = {
    "name": "CineHoyts Vivo San Fernardo",
    "tag": "vivo-san-fernando",
    "id": "vivo-san-fernando",
}
SAN_FERNARDO = {"tag": "san-fernardo", "list": [VIVO_SAN_FERNARDO]}

PLAZA_MAULE_TALCA = {
    "name": "CineHoyts Plaza Maule Talca",
    "tag": "plaza-maule-talca",
    "id": "plaza-maule-talca",
}
TALCA = {"tag": "talca", "list": [PLAZA_MAULE_TALCA]}

ARAUCO_CHILLAN = {
    "name": "CineHoyts Arauco Chillán",
    "tag": "arauco-chillan",
    "id": "arauco-chillan",
}
CHILLAN = {"tag": "chillan", "list": [ARAUCO_CHILLAN]}

MALLPLAZA_LOS_ANGELES = {
    "name": "CineHoyts MallPlaza Los Ángeles",
    "tag": "mallplaza-los-angeles",
    "id": "mallplaza-los-angeles",
}
LOS_ANGELES = {"tag": "los-angeles", "list": [MALLPLAZA_LOS_ANGELES]}

VIVO_OUTLET_TEMUCO = {
    "name": "Cinepolis Vivo Outlet Temuco",
    "tag": "cinepolis-vivo-outlet-temuco",
    "id": "cinepolis-vivo-outlet-temuco",
}
TEMUCO_PARIS = {
    "name": "CineHoyts Temuco (Edificio París)",
    "tag": "temuco-(edificio-paris)",
    "id": "temuco-(edificio-paris)",
}
TEMUCO = {"tag": "temuco", "list": [VIVO_OUTLET_TEMUCO, TEMUCO_PARIS]}

PASEO_COSTANERA_PUERTO_MONTT = {
    "name": "Cinepolis Paseo Costanera Puerto Montt",
    "tag": "cinepolis-paseo-costanera-puerto-montt",
    "id": "cinepolis-paseo-costanera-puerto-montt",
}
PUERTO_MONTT = {"tag": "puerto-montt", "list": [PASEO_COSTANERA_PUERTO_MONTT]}

PASEO_CHILOE = {
    "name": "Cinepolis Paseo Chiloe",
    "tag": "cinepolis-paseo-chiloe",
    "id": "cinepolis-paseo-chiloe",
}
CHILOE = {"tag": "chiloe", "list": [PASEO_CHILOE]}

SUR_DE_CHILE = {
    "tag": "sur-de-chile",
    "list": [
        VIVO_SAN_FERNARDO,
        PLAZA_MAULE_TALCA,
        ARAUCO_CHILLAN,
        MALLPLAZA_LOS_ANGELES,
        VIVO_OUTLET_TEMUCO,
        TEMUCO_PARIS,
        PASEO_COSTANERA_PUERTO_MONTT,
        PASEO_CHILOE,
    ],
}
SUR_DE_CHILE_TAGS = [city["tag"] for city in SUR_DE_CHILE["list"]]

CINEMAS = {
    "norte-y-centro-de-chile": NORTE_Y_CENTRO_DE_CHILE,
    "santiago-centro": SANTIAGO_CENTRO,
    "santiago-oriente": SANTIAGO_ORIENTE,
    "santiago-norte-y-poniente": SANTIAGO_NORTE_Y_PONIENTE,
    "santiago-sur": SANTIAGO_SUR,
    "sur-de-chile": SUR_DE_CHILE,
}
CINEMAS_SANTIAGO = [
    "santiago-centro",
    "santiago-oriente",
    "santiago-norte-y-poniente",
    "santiago-sur",
]
CINEMA_CITIES = {
    "antofagasta": "norte-y-centro-de-chile",
    "calama": "norte-y-centro-de-chile",
    "coquimbo": "norte-y-centro-de-chile",
    "ovalle": "norte-y-centro-de-chile",
    "valparaiso": "norte-y-centro-de-chile",
    "quillota": "sur-de-chile",
    "talca": "sur-de-chile",
    "chillan": "sur-de-chile",
    "los-angeles": "sur-de-chile",
    "temuco": "sur-de-chile",
    "puerto-montt": "sur-de-chile",
    "chiloe": "sur-de-chile",
}

CINEMA_ZONES = [
    ANTOFAGASTA,
    CALAMA,
    COQUIMBO,
    OVALLE,
    VALPARAISO,
    QUILLOTA,
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO,
    SANTIAGO_CENTRO,
    SANTIAGO_ORIENTE,
    SANTIAGO_NORTE_Y_PONIENTE,
    SANTIAGO_SUR,
    SUR_DE_CHILE,
    SAN_FERNARDO,
    TALCA,
    CHILLAN,
    LOS_ANGELES,
    TEMUCO,
    PUERTO_MONTT,
    CHILOE,
]

CINEMAS_TAGS = [cinema["tag"] for city in CINEMA_ZONES for cinema in city["list"]]
CINEMA_ZONES_TAGS = [city["tag"] for city in CINEMA_ZONES]
