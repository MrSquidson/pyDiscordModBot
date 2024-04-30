import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

class treeCMD(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
       synced = await self.bot.tree.sync() 
    
    # Simple test command
    @app_commands.command(
        name="commandname",
        description="My first application Command",
)
    async def first_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

    
    # Purge Messages indiscriminately in a channel
    @app_commands.command(
        name="purgemsg",
        description="A command that deletes a specified message",
    )
    @app_commands.describe(
        amount="Amount of messages you want purged"
    )

    async def purge_command(self, interaction: discord.Interaction, amount: int, reason: str):
        self.channel = interaction.channel
        await interaction.response.send_message('Attempting to purge messages!', ephemeral=True)
        dltMsgAmount = await self.channel.purge(limit=amount, reason=reason)
        await interaction.followup.send(f'Deleted {len(dltMsgAmount)} Messages!', ephemeral=True)
    

    # Public User Info      
    @app_commands.command(name='user_info', description='Get info of any user in this server')
    @app_commands.describe(user='select a user')

    async def user_info(self, interaction: discord.Interaction, user: discord.Member):
        # roles = []
        # if not user:
        #     user =  interaction.message.author
        # for roles in interaction.user.roles:
        #     roles.append(str(interaction.role.mention))
        self.embed = discord.Embed(color=user.color, timestamp=interaction.message.created_at)
        self.embed.author(name='Username', value=user)
        self.embed.thumbnail(url=user.avatar.url)
        self.embed.footer()

        pass

    # Ban command and stuff
    @app_commands.command(name='ban', description='Ban a user')
    @has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, user: discord.memeber, *, reason=None):
        try:
            await interaction.user.ban(reason=reason)
            await interaction.send(f'User {user} has been banned')
        except Exception as e:
            print(e)
            await interaction.send('Cannot ban user')
    # If a user who is not allowed to ban try's the ban command    
    @ban.error
    async def ban_error(interaction, error): 
        #try:??
            if isinstance(error, commands.MissingPermissions):
                await interaction.send ("You do not have permession to ban")
            
    pass

        
        
async def setup(bot):
    await bot.add_cog(treeCMD(bot))
    # await bot.add_cog('treeCMD') # only to remove class