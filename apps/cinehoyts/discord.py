# bot.py
import os

import discord
from discord.ext import commands
from apps.cinehoyts.services import get_showings

TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='$cinehoyts ')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def ping(ctx):
    await ctx.send("pong")


@client.command()
async def horarios_peliculas(ctx, city: str, zone: str, date: str, movie: str):
    cinema = get_showings(city, zone, date, movie)
    await ctx.send(cinema)


client.run(TOKEN)
