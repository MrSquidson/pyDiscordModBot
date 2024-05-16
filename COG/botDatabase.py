import os
import discord
from discord.ext import commands
import csv
from csv import DictWriter


class Database(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    async def filepathExists(filepath):
        if os.path.exists(filepath) != True:
            os.makedirs(filepath)

    async def modAction(guildID:int, modID:int, *args, **kwargs):
        offenderID = kwargs.get('offenderID', 'None Given')
        timeStart = kwargs.get('timeStart', None)
        timeEnd = kwargs.get('timeEnd', None)
        action = kwargs.get('action', None)

        field_names = ['modID', 'offenderID', 'timeStart', 'timeEnd', 'action']
        filepath = os.path.expanduser(os.path.join('DB', str(guildID)))
        Database.filepathExists(filepath=filepath)

        if action == None:
            return 'ERR: No action specified'

        if not os.path.exists(filepath + '/punishments.csv'): # Hvis './DB/GuildID/punishments.csv' ikke 
            open(filepath+'/punishments.csv','x')
            with open((os.path.join(filepath, 'punishments.csv')),'w', newline='') as csvfile: #Opret ny csv fil
                writer = csv.DictWriter(csvfile, fieldnames=field_names) # Med field_names i headeren (indsætter også header)
                writer.writeheader()
                writer.writerow({f'modId': modID, 'offenderID': offenderID,'timeStart': timeStart,'timeEnd': timeEnd, 'action': action}) # Skriv case 1
                print('Made new .csv file for GuildID')

        else: # ... 'punishments.csv' findes!
            with open(filepath + '/punishments.csv','a', newline='') as f_object: # åben filen i append mode!
                dictwriter_object = DictWriter(f_object, fieldnames=field_names) # med de samme fieldnames som før
                dictwriter_object.writerow({modID, offenderID, timeStart, timeEnd, action}) # Skriv den nye case ind i filen
                print('Appended most recent case')

async def setup(bot) -> None:
     await bot.add_cog(Database(bot))