import os
import random
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

# DO NOT TOUCH, WE DON'T WHAT WE DID, BUT IT WORKS NOW!!!!!
# Chooses one of the Random Activities(tm)
async def randact():
    randAct = True
    while randAct == True:
        chance = random.randint(0,1)
        if chance == 0: # Makes the bot activity say that it's "Listening to Commands"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Commands"))
            print('0')
            randAct = False
        elif chance == 1: # Makes the bot activity as that it's "Watching you"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
            print('1')
            randAct = False


@bot.event
async def on_ready():
    await bot.tree.sync()
    await randact()
    print(f'Logged on as {bot.user}!')

#Kør botten
bot.run(TOKEN)
