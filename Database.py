import os
import discord
import csv


class Database:
    def __init__(self) -> None:
        pass
            # Check if the folder already exists
        if not os.path.exists(os.path.join('./DB', discord.Guild.id)):
            #Laver en filepath til brug senere
            filepath = os.path.join(os.path.join('./DB', discord.Guild.id))            
            # Save cleaned content to file
            with open(filepath, 'w', encoding='utf-8') as csv_file:
                pass
    
    def modAction(self, guild, modID, offenderID, action):
        if os.path.exists(os.path.join('./DB', guild, 'punishments.csv')):
            csv.writer()