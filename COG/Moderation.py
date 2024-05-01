import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import typing

intents = discord.Intents.default()
intents.message_content = True
class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready():
        print('Loaded??') 
    
    # Simple test command
    @app_commands.command(
        name="commandname",
        description="My first application Command",
)
    async def first_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

    # Public User Info      
    @app_commands.command(
        name='user_info', 
        description='Get info of any user in this server',
    )
    @app_commands.describe(
        user='select a user'
    )

    async def userinfo(self, interaction: discord.Interaction, user: Member):
        self.embed = discord.Embed(title=f"User Info about {user}")
        self.embed.author(name='Username', value=user.name)
        self.embed.thumbnail(url=user.avatar.url)
        self.embed.add_field(name='Discord @', value=user.discriminator)
        self.embed.add_field(name='UserID', value=user.id)
        self.embed.add_field(name='Current status', value=user.status)
        self.embed.add_field(name='Server Join', value=user.joined_at)
        self.embed.add_field(name='Account age', value=user.created_at)
        await interaction.followup.send(embed=self.embed)
    
    # Purge Messages indiscriminately in a channel
    @app_commands.command(
        name="purgemsg_1",
        description="A command that deletes a specified message",
    )
    @app_commands.describe(
        amount="Amount of messages you want purged"
    )
    @app_commands.describe(
        reason='The Reason'
    )

    async def purge_command(self, interaction: discord.Interaction, amount: int, reason: str):
        self.channel = interaction.channel
        await interaction.response.send_message('Attempting to purge messages!', ephemeral=True)
        dltMsgAmount = await self.channel.purge(limit=amount, reason=typing.Optional[app_commands.Choice[str]])
        await interaction.followup.send(f'Deleted {len(dltMsgAmount)} Messages!', ephemeral=True)
    

    # Ban command and stuff
    # @app_commands.command(name='ban', description='Ban a user')
    # @app_commands.describe(name='reason', description='give a reason for ban')
    # @has_permissions(ban_members = True)
    # async def ban(self, interaction: discord.Interaction, user: Member, reason: str):
    #     try:
    #         await interaction.user.ban(reason=reason)
    #         await interaction.response.send_message(f'User {user} has been banned')
    #     except Exception as e:
    #         print(e)
    #         await interaction.response.send_message('Cannot ban user')            
    # pass

        
        
async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
    # await bot.add_cog('treeCMD') # only to remove class