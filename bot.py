import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

option = app_commands.AppCommand.options

import time
# I need a comment...
# Indlæser .env filen så den kan bruges
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="<<", intents=discord.Intents.all())

# # Test cmd that comes with library
# @bot.tree.command(
#     name="commandname",
#     description="My first application Command",
# )
# async def first_command(interaction):
#     await interaction.response.send_message("Hello!")



# #Purge Messages indiscriminately in a channel
@bot.tree.command(
    name="purgemsg",
    description="A command that deletes a specified message",

)
@app_commands.describe(
    amount="Amount of messages you want purged"
)
@app_commands.describe(
    reason="The reason why you're purging messages"
)
async def delete_command(interaction: discord.Interaction, amount: int,reason: str):
    channel = interaction.channel

    deleted = await channel.purge(limit=amount, reason = reason)
    await interaction.response.send_message(f"Deleted {len(deleted)} Messages!", ephemeral=True)

# VIRKER IKKE ENDNU
# @bot.tree.command(
#         name="sync",
#         description="Syncs discord commands",
#         guild=discord.Object(id=867851000286806016)
# )
# async def sync(interaction: discord.Interaction):
#     try:
#         await interaction.response.send_message('Syncing...')
#         await bot.tree.sync()
#         await interaction.response.send_message('Synced!')
#     except:
#         await interaction.response.send_message('Syncing Failed')

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
    synced = await bot.tree.sync()
    await randact()
    print(f'Logged on as {bot.user}!')
    print(f'synced {len(synced)}')

#Kør botten
bot.run(TOKEN)
