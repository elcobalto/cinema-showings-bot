MALLPLAZA_ARICA = {
    "name": "Cinemark MallPlaza Arica",
    "tag": "cinemark-mallplaza-arica",
    "id": 2305,
}
ARICA = {"tag": "arica", "list": [MALLPLAZA_ARICA]}

MALLPLAZA_IQUIQUE = {
    "name": "Cinemark MallPlaza Iquique",
    "tag": "mallplaza-iquique",
    "id": 520,
}
IQUIQUE = {"tag": "iquique", "list": [MALLPLAZA_IQUIQUE]}

MALLPLAZA_LA_SERENA = {
    "name": "Cinemark MallPlaza La Serena",
    "tag": "mallplaza-la-serena",
    "id": 2309,
}
LA_SERENA = {"tag": "la-serena", "list": [MALLPLAZA_LA_SERENA]}

OPEN_OVALLE = {"name": "Cinemark Open Ovalle", "tag": "open-ovalle", "id": 2304}
OVALLE = {"tag": "ovalle", "list": [OPEN_OVALLE]}

OPEN_LA_CALERA = {
    "name": "Cinemark Open La Calera",
    "tag": "open-la-calera",
    "id": 2308,
}
LA_CALERA = {"tag": "la-calera", "list": [OPEN_LA_CALERA]}

ESPACIO_URBANO = {"name": "Cinemark Espacio Urbano", "tag": "espacio-urbano", "id": 514}
MALL_MARINA = {"name": "Cinemark MallMarina", "tag": "mall-marina", "id": 570}
VINA_DEL_MAR = {
    "name": "Cinemark Viña del Mar",
    "tag": "viña-del-mar",
    "list": [ESPACIO_URBANO, MALL_MARINA],
}

NORTE_Y_CENTRO_DE_CHILE = {
    "tag": "norte-y-centro-de-chile",
    "list": [
        MALLPLAZA_ARICA,
        MALLPLAZA_IQUIQUE,
        MALLPLAZA_LA_SERENA,
        OPEN_OVALLE,
        OPEN_LA_CALERA,
        ESPACIO_URBANO,
        MALL_MARINA,
    ],
}

ALTO_LAS_CONDES = {
    "name": "Cinemark Alto las Condes",
    "tag": "alto-las-condes",
    "id": 512,
}
MALLPLAZA_NORTE = {
    "name": "Cinemark MallPlaza Norte",
    "tag": "mallplaza-norte",
    "id": 572,
}
MALLPLAZA_OESTE = {
    "name": "Cinemark MallPlaza Oeste",
    "tag": "mallplaza-oeste",
    "id": 513,
}
MALLPLAZA_TOBALABA = {
    "name": "Cinemark MallPlaza Tobalaba",
    "tag": "mallplaza-tobalaba",
    "id": 519,
}
MALLPLAZA_VESPUCIO = {
    "name": "Cinemark MallPlaza Vespucio",
    "tag": "mallplaza-vespucio",
    "id": 511,
}
MID_MALL_MAIPU = {
    "name": "Cinemark Mid Mall Maipú",
    "tag": "mid-mall-maipu",
    "id": 2307,
}
PORTAL_NUNOA = {"name": "Cinemark Portal Ñuñoa", "tag": "portal-nunoa", "id": 2300}
SANTIAGO = {
    "tag": "santiago",
    "list": [
        ALTO_LAS_CONDES,
        MALLPLAZA_NORTE,
        MALLPLAZA_OESTE,
        MALLPLAZA_TOBALABA,
        MALLPLAZA_VESPUCIO,
        MID_MALL_MAIPU,
        PORTAL_NUNOA,
    ],
}
SANTIAGO_CENTRO = {
    "tag": "santiago-centro",
    "list": [],
}
SANTIAGO_ORIENTE = {
    "tag": "santiago-oriente",
    "list": [
        ALTO_LAS_CONDES,
        PORTAL_NUNOA,
    ],
}
SANTIAGO_NORTE_Y_PONIENTE = {
    "tag": "santiago-norte-y-poniente",
    "list": [
        MALLPLAZA_NORTE,
        MALLPLAZA_OESTE,
        MID_MALL_MAIPU,
    ],
}
SANTIAGO_SUR = {
    "tag": "santiago-sur",
    "list": [
        MALLPLAZA_TOBALABA,
        MALLPLAZA_VESPUCIO,
    ],
}

OPEN_RANCAGUA = {"name": "Cinemark Open Rancagua", "tag": "open-rancagua", "id": 2303}
MALL_RANCAGUA = {"name": "Cinemark Mall Rancagua", "tag": "mall-rancagua", "id": 517}
RANCAGUA = {"tag": "rancagua", "list": [OPEN_RANCAGUA, MALL_RANCAGUA]}

MALLPLAZA_TREBOL = {
    "name": "Cinemark MallPlaza Trebol",
    "tag": "mallplaza-trebol",
    "id": 548,
}
TALCAHUANO = {"tag": "talcahuano", "list": [MALLPLAZA_TREBOL]}

MALLPLAZA_MIRADOR_BIO_BIO = {
    "name": "Cinemark MallPlaza Mirador Bio-Bio",
    "tag": "mallplaza-mirador-bio-bio",
    "id": 2302,
}
CONCEPCION = {"tag": "concepcion", "list": [MALLPLAZA_MIRADOR_BIO_BIO]}

ARAUCO_CORONEL = {
    "name": "Cinemark Arauco Coronel",
    "tag": "arauco-coronel",
    "id": 2306,
}
CORONEL = {"tag": "coronel", "list": [ARAUCO_CORONEL]}

GRAN_CONCEPCION = {
    "tag": "gran-concepcion",
    "list": [MALLPLAZA_TREBOL, MALLPLAZA_MIRADOR_BIO_BIO, ARAUCO_CORONEL],
}

PORTAL_OSORNO = {"name": "Cinemark Portal Osorno", "tag": "portal-osorno", "id": 2301}
OSORNO = {"tag": "osorno", "list": [PORTAL_OSORNO]}

SUR_DE_CHILE = {
    "tag": "sur-de-chile",
    "list": [
        OPEN_RANCAGUA,
        MALL_RANCAGUA,
        MALLPLAZA_TREBOL,
        MALLPLAZA_MIRADOR_BIO_BIO,
        ARAUCO_CORONEL,
        PORTAL_OSORNO,
    ],
}

CINEMA_ZONES = [
    ARICA,
    IQUIQUE,
    LA_SERENA,
    OVALLE,
    LA_CALERA,
    VINA_DEL_MAR,
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO,
    SANTIAGO_CENTRO,
    SANTIAGO_ORIENTE,
    SANTIAGO_NORTE_Y_PONIENTE,
    SANTIAGO_SUR,
    RANCAGUA,
    TALCAHUANO,
    CONCEPCION,
    CORONEL,
    GRAN_CONCEPCION,
    OSORNO,
    SUR_DE_CHILE,
]

CINEMA_MACROZONES = [
    NORTE_Y_CENTRO_DE_CHILE,
    SANTIAGO_CENTRO,
    SANTIAGO_ORIENTE,
    SANTIAGO_NORTE_Y_PONIENTE,
    SANTIAGO_SUR,
    SUR_DE_CHILE,
]

CINEMAS_TAGS = [cinema["tag"] for city in CINEMA_ZONES for cinema in city["list"]]
CINEMA_ZONES_TAGS = [city["tag"] for city in CINEMA_ZONES]

TOTAL_CINEMAS_TAGS = [
    cinema["tag"] for city in CINEMA_MACROZONES for cinema in city["list"]
]
TOTAL_CINEMA_ZONES_TAGS = [city["tag"] for city in CINEMA_MACROZONES]
