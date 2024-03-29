# bot.py
import os

from discord import Intents
from discord.ext import commands

from apps.discord import (
    get_cinema_total,
    get_format_total,
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

    intents = Intents.all()
    client = commands.Bot(command_prefix=COMMAND, intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.command()
    async def horarios(
        ctx, movie: str, date: str, cinema: str = None, format: str = None
    ):
        movie = None if not movie or movie in ("skip", "sk", "sp") else movie.lower()
        date = None if not date or date in ("skip", "sk", "sp") else date.lower()
        cinema = (
            None if not cinema or cinema in ("skip", "sk", "sp") else cinema.lower()
        )
        format = None if not format else format.upper()
        if not movie and date and cinema:
            message, total = get_general_cinema_showings(cinema, date, format)
        elif movie and not date and cinema:
            message, total = get_movie_date_message(
                get_showing_by_cinema(movie, cinema, format), "CINEMA"
            )
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
    async def total_formatos(ctx, date, format: str = None):
        message = get_format_total(date, format)
        await ctx.send(message)

    @client.command()
    async def total_cinemas(ctx, date, format: str = None):
        message = get_cinema_total(date, format)
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
        info += "$c.total fecha\nRECUENTO DE PELÍCULAS TOTALES POR FECHA.\n\n"
        info += "$c.info_cities\nLISTA DE ZONAS INCLUIDAS.\n\n"
        info += "$c.info_cinemas\nLISTA DE CINES INCLUIDOS.\n\n"
        await ctx.send(info)

    if TOKEN:
        client.run(TOKEN)
