# bot.py
import os

from discord.ext import commands

from apps.cinehoyts.services import get_info_cinemas, get_info_cities, get_showings, get_movie_showing_by_date, get_movie_showing_by_cinema


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
    async def horarios_cine(ctx, city: str, date: str, movie: str):
        cinema_showings = get_showings(city, date, movie)
        await ctx.send(cinema_showings)


    @client.command()
    async def horarios_pelicula(ctx, date: str, movie: str):
        cinema_showings = get_movie_showing_by_date(date, movie)
        for cinema_showing_part in cinema_showings.split("$SEPARATOR$"):
            if cinema_showing_part:
                await ctx.send(cinema_showing_part)


    @client.command()
    async def fechas_pelicula(ctx, cinema: str, movie: str):
        cinema_showings = get_movie_showing_by_cinema(cinema, movie)
        for cinema_showing_part in cinema_showings.split("$SEPARATOR$"):
            if cinema_showing_part:
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
