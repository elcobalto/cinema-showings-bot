ESPACIO_URBANO_ANTOFAGASTA = "cinehoyts-espacio-urbano-antofagasta"
OVALLE = "cinepolis-ovalle"
SHOPPING_QUILLOTA = "cinepolis-shopping-quillota"
VIVO_COQUIMBO = "cinepolis-vivo-coquimbo"
MALLPLAZA_ANTOFAGASTA = "mallplaza-antofagasta"
MALL_PLAZA_CALAMA = "mallplaza-calama"
VALPARAISO = "valparaiso"
NORTE_Y_CENTRO_DE_CHILE = [
    ESPACIO_URBANO_ANTOFAGASTA,
    OVALLE,
    SHOPPING_QUILLOTA,
    VIVO_COQUIMBO,
    MALLPLAZA_ANTOFAGASTA,
    MALL_PLAZA_CALAMA,
    VALPARAISO,
]


ARAUCO_ESTACION = "arauco-estacion"
VIVO_IMPERIO = "cinepolis-vivo-imperio"
SANTIAGO_CENTRO = [ARAUCO_ESTACION, VIVO_IMPERIO]

CASA_COSTANERA = "cinepolis-casa-costanera"
LA_REINA = "cinepolis-la-reina"
MALLPLAZA_EGANA = "cinepolis-mallplaza-egana"
MALLPLAZA_EGANA_PREMIUM_CLASS = "cinepolis-mallplaza-egana-premium-class"
MALLPLAZA_LOS_DOMINICOS = "cinepolis-mallplaza-los-dominicos"
MALLPLAZA_LOS_DOMINICOS_PREMIUM_CLASS = (
    "cinepolis-mallplaza-los-dominicos-premium-class"
)
CINEPOLIS_PASEO_LOS_TRAPENSES = "cinepolis-paseo-los-trapenses"
PARQUE_ARAUCO = "parque-arauco"
PARQUE_ARAUCO_PREMIUM_CLASS = "parque-arauco-premium-class"
PASEO_LOS_DOMINICOS = "paseo-los-dominicos-(san-carlos)"
SANTIAGO_ORIENTE = [
    CASA_COSTANERA,
    LA_REINA,
    MALLPLAZA_EGANA,
    MALLPLAZA_EGANA_PREMIUM_CLASS,
    MALLPLAZA_LOS_DOMINICOS,
    MALLPLAZA_LOS_DOMINICOS_PREMIUM_CLASS,
    CINEPOLIS_PASEO_LOS_TRAPENSES,
    PARQUE_ARAUCO,
    PARQUE_ARAUCO_PREMIUM_CLASS,
    PASEO_LOS_DOMINICOS,
]


ARAUCO_MAIPU = "arauco-maipu"
ARAUCO_QUILICURA = "arauco-quilicura"
PATIO_OUTLET_MAIPU = "cinepolis-patio-outlet-maipu"
ESPACIO_URBANO_MELIPILLA = "espacio-urbano-melipilla"
SANTIAGO_PONIENTE = [
    ARAUCO_MAIPU,
    ARAUCO_QUILICURA,
    PATIO_OUTLET_MAIPU,
    ESPACIO_URBANO_MELIPILLA,
]

ESPACIO_URBANO_PUENTE_ALTO = "cinepolis-espacio-urbano-puente-alto"
PATIO_OUTLET_LA_FLORIDA = "cinepolis-patio-outlet-la-florida"
PLAZUELA_INDEPENDENCIA_PUENTE_ALTO = "cinepolis-plazuela-independencia-puente-alto"
MALLPLAZA_SUR = "mallplaza-sur"
PASEO_SAN_BERNARDO = "paseo-san-bernardo"
SANTIAGO_SUR = [
    ESPACIO_URBANO_PUENTE_ALTO,
    PATIO_OUTLET_LA_FLORIDA,
    PLAZUELA_INDEPENDENCIA_PUENTE_ALTO,
    MALLPLAZA_SUR,
    PASEO_SAN_BERNARDO,
]

ARAUCO_CHILLAN = "arauco-chillan"
PASEO_CHILOE = "cinepolis-paseo-chiloe"
PASEO_COSTANERA_PUERTO_MONTT = "cinepolis-paseo-costanera-puerto-montt"
VIVO_OUTLET_TEMUCO = "cinepolis-vivo-outlet-temuco"
MALLPLAZA_LOS_ANGELES = "mallplaza-los-angeles"
PLAZA_MAULE_TALCA = "plaza-maule-talca"
TEMUCO_PARIS = "temuco-(edificio-paris)"
VIVO_SAN_FERNARDO = "vivo-san-fernando"
SUR_DE_CHILE = [
    ARAUCO_CHILLAN,
    PASEO_CHILOE,
    PASEO_COSTANERA_PUERTO_MONTT,
    VIVO_OUTLET_TEMUCO,
    MALLPLAZA_LOS_ANGELES,
    PLAZA_MAULE_TALCA,
    TEMUCO_PARIS,
    VIVO_SAN_FERNARDO,
]

CINEMAS = {
    "norte-y-centro-de-chile": NORTE_Y_CENTRO_DE_CHILE,
    "santiago-centro": SANTIAGO_CENTRO,
    "santiago-oriente": SANTIAGO_ORIENTE,
    "santiago-norte-y-poniente": SANTIAGO_PONIENTE,
    "santiago-sur": SANTIAGO_SUR,
    "sur-de-chile": SUR_DE_CHILE,
}

CINEMA_ZONES = [
    "norte-y-centro-de-chile",
    "santiago-centro",
    "santiago-oriente",
    "santiago-norte-y-poniente",
    "santiago-sur",
    "sur-de-chile",
]
