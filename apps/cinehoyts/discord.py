# bot.py
import os

from discord.ext import commands

from apps.cinehoyts.services import get_info_cinemas, get_info_cities, get_showings

TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="$cartelera ")


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.command()
async def ping(ctx):
    await ctx.send("pong")


@client.command()
async def horarios_peliculas(ctx, city: str, date: str, movie: str):
    cinema = get_showings(city, date, movie)
    await ctx.send(cinema)


@client.command()
async def info_cities(ctx, zone):
    cities = get_info_cities(zone)
    await ctx.send(cities)


@client.command()
async def info_cinemas(ctx):
    cinemas = get_info_cinemas()
    await ctx.send(cinemas)


client.run(TOKEN)
