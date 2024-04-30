import os
import discord
import csv
from csv import DictWriter


class Database:
    filepath = os.path.join('./DB', discord.Guild.id)

    def __init__(self) -> None:
        #Laver en filepath til brug senere
        pass

    def modAction(self, filepath, guildID:int, modID:int, offenderID:int, timeStart:int, timeEnd:int, action:str):
        field_names = ['modID', 'offenderID', 'timeStart', 'timeEnd', 'action']

        if not os.path.exists(os.path.join(filepath, 'punishments.csv')): # Hvis './DB/GuildID/punishments.csv' ikke findes
            with open((os.path.join(filepath, 'punishments.csv')),'w', newline='') as csvfile: #Opret ny csv fil
                writer = csv.DictWriter(csvfile, fieldnames=field_names) # Med field_names i headeren (indsætter også header)
                writer.writeheader()
                writer.writerow({f'modId': modID, 'offenderID': offenderID,'timeStart': timeStart,'timeEnd': timeEnd, 'action': action}) # Skriv case 1
                print('Made new .csv file for GuildID')

        else: # ... 'punishments.csv' findes!
            with open((os.path.join(filepath, 'punishments.csv')),'a', newline='') as f_object: # åben filen i append mode!
                dictwriter_object = DictWriter(f_object, fieldnames=field_names) # med de samme fieldnames som før
                dictwriter_object.writerow({modID, offenderID, timeStart, timeEnd, action}) # Skriv den nye case ind i filen
                print('Appended most recent case')

