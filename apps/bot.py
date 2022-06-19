# bot.py
import os

from discord.ext import commands

from apps import (
    get_general_cinema_showings,
    get_general_showings,
    get_info_cinemas,
    get_info_cities,
    get_movie_date_message,
    get_showing_by_cinema,
    get_total,
)
from cinema_showings_bot.settings import COMMAND


def main():
    TOKEN = os.getenv("DISCORD_TOKEN", "")

    client = commands.Bot(command_prefix=COMMAND)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.command()
    async def horarios(ctx, movie: str, date: str, cinema: str = None, format: str = None):
        movie = None if movie in ('skip', 'sk', 'sp') else movie
        date = None if date in ('skip', 'sk', 'sp') else date
        cinema = None if cinema in ('skip', 'sk', 'sp') else cinema
        if not movie and date and cinema:
            message, total = get_general_cinema_showings(cinema, date, format)
        elif movie and not date and cinema:
            message, total = get_movie_date_message(get_showing_by_cinema(movie, cinema, format), "CINEMA")
        else:
            message, total = get_general_showings(movie, date, cinema, format)
        message = f"{total} HORARIOS EN TOTAL \n——————\n{message}"
        for cinema_showing_part in message.split("$SEPARATOR$"):
            if cinema_showing_part and cinema_showing_part not in ("\n", "\n\n"):
                await ctx.send(cinema_showing_part)


    @client.command()
    async def total(ctx, date, format: str = None):
        message = get_total(date, format)
        await ctx.send(message)

    @client.command()
    async def info_cities(
        ctx,
    ):
        cities = get_info_cities()
        await ctx.send(cities)

    @client.command()
    async def info_cinemas(ctx):
        cinemas = get_info_cinemas()
        await ctx.send(cinemas)

    @client.command()
    async def info(ctx):
        info = "$c.horarios nombre-pelicula fecha nombre-cine(opcional)\nHORARIOS PELÍCULA PARA UNA FECHA EN PARTICULAR. EN UN CINE O TODOS LOS CINES. NOMBRE DEL CINE TAMBIÉN PUEDE SER UNA ZONA.\n\n"
        info += "$c.horarios_cine nombre-pelicula nombre-cine\nHORARIOS PELÍCULA PARA UN CINE EN PARTICULAR.\n\n"
        info += "$c.cine nombre-cine fecha(opcional)\nCARTELERA COMPLETA DE UN CINE. EN GENERAL O PARA UN DÍA EN PARTICULAR.\n\n"
        info += "$c.total fecha\nRECUENTO DE PELÍCULAS TOTALES POR FECHA.\n\n"
        info += "$c.info_cities\nLISTA DE ZONAS INCLUIDAS.\n\n"
        info += "$c.info_cinemas\nLISTA DE CINES INCLUIDOS.\n\n"
        await ctx.send(info)

    if TOKEN:
        client.run(TOKEN)
