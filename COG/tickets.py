import discord
from discord import app_commands
from discord.ext import commands
import os
import csv

filepath = os.path.expanduser(os.path.join('Documents\GitHub\pyDicordModBot\DB', str(discord.Guild.id), 'tickets'))
ticCat = (str(os.path.join(filepath, 'ticCat.txt')))
ticketLogs = (str(os.path.join(filepath, 'ticketLogs.txt')))

class ticket(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    async def filepathExists(filepath):
        if os.path.exists(filepath) != True:
            os.makedirs(filepath)
    
    @commands.Cog.listener()
    async def on_ready(self):
       await self.bot.tree.sync() 

    # Simple test command
    @app_commands.command(
        name="ticketscommandname",
        description="My first application Command"
)
    async def first_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")



    
    # Set ticket category
    @app_commands.command(
            name='ticketcat', 
            description='Set the Ticket Category'
            )
    @app_commands.checks.has_permissions(administrator=True)
    async def ticCat(self, interaction: discord.Interaction,category:str):
        # Update the Guild ID in the DB path for current call
        current_dir = os.getcwd()
        filepath = os.path.expanduser(os.path.join(current_dir, 'DB', str(interaction.guild.id), 'tickets'))
        os.makedirs(filepath)
        if ticket.filepathExists(filepath=filepath) != True:
            print(f'\n\nFailed to setup filepath for guild: {interaction.guild.name} \n Filepath used: {filepath} \n Guild ID: {interaction.guild.id}\n\n')
        ticCat = (str(os.path.join(filepath, 'ticCat.txt')))

        # Open the ticket Category txt file in writing mode
        if os.path.exists(ticCat) == False:
            open(ticCat,'x')
        with open(ticCat, 'w') as txtfile: # Writes or Overwrites a txtfile with the Category id
            # Write the called category ID into the document
            txtfile.write(str(category))
            txtfile.close()

        # Sets up a log for tickets in the Database if it doesn't exist
        if (os.path.exists(os.path.join(filepath, 'ticketLogs.csv'))) != True:
            open(os.path.join(filepath, 'ticketLogs.csv'),'x')
            with open(str(os.path.join(filepath, 'ticketLogs.csv')),'w', newline='') as csvfile:
                field_names = ['UserID', 'ticketID', 'Action', 'Reason']
                writer = csv.DictWriter(csvfile, fieldnames=field_names) # Med field_names i headeren (indsætter også header)
                writer.writeheader()
        await interaction.response.send_message('Ticket Category Set!', ephemeral=True)





    #Open ticket
    @app_commands.command(
            name='openticket', 
            description='Opens a ticket'
            )
    async def openTicket(self, interaction: discord.Interaction):
        guild = discord.Guild.id 
        filepath = os.path.expanduser(os.path.join('DB', str(interaction.guild.id), 'tickets'))
        ticCat = (str(os.path.join(filepath, 'ticCat.txt')))

        if (os.path.exists(ticCat)) != True:
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

async def setup(bot) -> None:
    await bot.add_cog(ticket(bot))