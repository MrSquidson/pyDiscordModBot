import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import typing

option = app_commands.AppCommand.options

dbname = 'DB'

import time
# I need a comment...
# Indlæser .env filen så den kan bruges
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="<<", intents=intents)

# # Test cmd that comes with library
# @bot.tree.command(
#     name="commandname",
#     description="My first application Command",
# )
# async def first_command(interaction):
#     await interaction.response.send_message("Hello!")
    

# Sync Kommando - Syncronisere det nuværende kommando træ med det vi arbejder på.
@bot.tree.command(
    name="sync_cmd",
    description="Syncs discord commands",
)
async def sync(interaction: discord.Interaction):
    try:
        await interaction.response.send_message('Syncing...', ephemeral=True)
        i = 0
        for filename in os.listdir('./COG'):
            if filename.endswith('.py'):
                i += 1        
                await bot.reload_extension(f'COG.{filename[:-3]}')
                print(f'Syncing {filename}...')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {i} cogs and {len(synced)} commands')
        except Exception as e:
            print(e)
        await interaction.followup.send(f'Synced {i} cogs and {len(synced)} commands! :D', ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.followup.send('Syncing Failed :c', ephemeral=True)


# DO NOT TOUCH, WE DON'T WHAT WE DID, BUT IT WORKS NOW!!!!!
# Chooses one of the Random Activities(tm)
async def randact():
    randAct = True
    while randAct == True:
        chance = random.randint(0,1)
        if chance == 0: # Makes the bot activity say that it's "Listening to Commands"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Commands"))
            print('Activity set to: Listening to Commands')
            randAct = False
        elif chance == 1: # Makes the bot activity as that it's "Watching you"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
            print('Activity set to: Watching you')
            randAct = False


@bot.event
async def on_ready(): 
    await randact()
    i = 0
    for filename in os.listdir('./COG'):
        if filename.endswith('.py'):            
            i += 1
            await bot.load_extension(f'COG.{filename[:-3]}')
            print(f'Loading COG.{filename[:-3]}...')
    print(f"Loaded {i} cog's on startup!")
    print(f'Logged on as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)}')
    except Exception as e:
        print(e)

@bot.event
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You dont have all the requirements :angry:")


#Kør botten
bot.run(TOKEN)
