import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import time

#Indlæser .env filen så den kan bruges
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="<<", intents=discord.Intents.all())


@bot.tree.command(
    name="commandname",
    description="My first application Command",
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")


@bot.event
async def on_ready():
    await bot.tree.sync()
    bot.change_presence(activity=discord.Game("It's Modding Time"))
    print(f'Logged on as {bot.user}!')

#Kør botten
bot.run(TOKEN)
