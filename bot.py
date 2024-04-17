import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import time

#Indlæser .env filen så den kan bruges
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="<<", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

intents = discord.Intents.default()
intents.message_content = True

#Kør botten
bot.run(TOKEN)
