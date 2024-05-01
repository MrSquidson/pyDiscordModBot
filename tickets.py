import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import os
import csv
from csv import DictWriter

filepath = (str(os.path.join('./DB', str(discord.Guild.id), '/tickets')))
ticCat = (str(os.path.join(filepath, 'ticCat.txt')))
ticketLogs = (str(os.path.join(filepath, 'ticketLogs.txt')))

class ticket(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
       synced = await self.bot.tree.sync() 

    try:
        # Simple test command
        @app_commands.command(
            name="ticketscommandname",
            description="My first application Command",
    )
        async def first_command(self, interaction: discord.Interaction):
            await interaction.response.send_message("Hello!")
    except:
        print('Failed to compile the basic hello world cmd wtf!')

    try:
        # Set ticket category
        @app_commands.command(name='ticketcat', description='Set the Ticket Category')
        @app_commands.describe(
            category="Category ID"
        )
        @commands.has_permissions(manage_guild=True)
        async def ticCat(self, category:int, interaction: discord.Interaction):
            filepath = str(os.path.join('./DB', discord.Guild.id, '/tickets'))
            with open((str(os.path.join(filepath, 'ticCat.txt'))), 'w') as txtfile: # Writes or Overwrites a txtfile with the Category id
                txtfile.write(category)
                txtfile.close()

            # Sets up a log for tickets in the Database if it doesn't exist
            if (os.path.exists(os.path.join(filepath, 'ticketLogs.csv'))) != True:
                with open(str(os.path.join(filepath, 'ticketLogs.csv')),'w', newline='') as csvfile:
                    field_names = ['UserID', 'ticketID', 'Action', 'Reason']
                    writer = csv.DictWriter(csvfile, fieldnames=field_names) # Med field_names i headeren (indsætter også header)
                    writer.writeheader()
            await interaction.followup.send('Ticket Category Set!', ephemeral=True)
    except:
        print('Failed to compile ticketcat cmd')



    try:
        #Open ticket
        @app_commands.command(name='openticket', description='Opens a ticket')
        async def openTicket(ticCat,ticketLogs, interaction: discord.Interaction):
            guild = discord.guild.id 
            if (os.path.exists(os.path.join(filepath, 'ticCat.txt'))) != True:
                await interaction.followup.send('Error! Missing Ticket Category... Please add a ticket category through /ticketCat', ephemeral=True)
            else:
                await interaction.followup.send('Attempting to open a ticket...')
                ticketCount = 0
                openCatId = open(ticCat, 'r')
                catID = openCatId.readlines()

                #Count the amount of created tickets
                with open(ticketLogs, 'r', encoding='utf-8', newline='') as f:
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    #print(dialect)
                    # Move to beginning of file
                    f.seek(0)
                    # DictReader uses the first row in the file as headers.
                    r = csv.DictReader(f, dialect=dialect)
                    for row in r:
                        if row['Action'] in 'Created':
                            ticketCount += 1
                

                await discord.Guild.create_text_channel(
                    name=f'ticket-'+str(ticketCount+1), 
                    category=catID, 
                    overwrites = {
                    await guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    await guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    await guild.get_member(interaction.user): discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        }
                )
                await interaction.followup.send(f'Opened Ticket!')
    except:
        print('Failed to Compile openticket cmd')

