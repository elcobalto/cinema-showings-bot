# bot.py
import os

from discord.ext import commands

from apps.cinehoyts.services import (
    get_info_cinemas,
    get_info_cities,
    get_showing_by_cinema,
    get_showing_by_date,
    get_showings,
    get_showings_by_zone,
    get_cinema_showings,
    get_cinema_showings_by_date,
)
from apps.cinehoyts.constants import CINEMAS_ZONES


def main():
    TOKEN = os.getenv("DISCORD_TOKEN")

    client = commands.Bot(command_prefix="$c.")

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.command()
    async def ping(ctx):
        await ctx.send("pong")

    @client.command()
    async def horarios(ctx, movie: str, date: str, cinema: str = None):
        cinema_is_zone = cinema in CINEMAS_ZONES
        if cinema and not cinema_is_zone:
            cinema_showings = get_showings(movie, date, cinema)
        elif cinema and cinema_is_zone:
            cinema_showings = get_showings_by_zone(movie, date, cinema)
        else:
            cinema_showings = get_showing_by_date(movie, date)
        for cinema_showing_part in cinema_showings.split("$SEPARATOR$"):
            if cinema_showing_part and cinema_showing_part not in ('\n', '\n\n'):
                await ctx.send(cinema_showing_part)

    @client.command()
    async def horarios_cine(ctx, movie: str, cinema: str, format: str = None):
        cinema_showings = get_showing_by_cinema(movie, cinema, format)
        for cinema_showing_part in cinema_showings.split("$SEPARATOR$"):
            if cinema_showing_part and cinema_showing_part not in ('\n', '\n\n'):
                await ctx.send(cinema_showing_part)

    @client.command()
    async def cine(ctx, cinema: str, date: str = None):
        if date:
            cinema_showings = get_cinema_showings_by_date(cinema, date)
        else:
            cinema_showings = get_cinema_showings(cinema)
        for cinema_showing_part in cinema_showings.split("$SEPARATOR$"):
            if cinema_showing_part and cinema_showing_part not in ('\n', '\n\n'):
                await ctx.send(cinema_showing_part)

    @client.command()
    async def info_cities(ctx, zone):
        cities = get_info_cities(zone)
        await ctx.send(cities)

    @client.command()
    async def info_cinemas(ctx):
        cinemas = get_info_cinemas()
        await ctx.send(cinemas)

    client.run(TOKEN)