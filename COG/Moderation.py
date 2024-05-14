import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
import datetime
from discord.ext.commands import has_permissions, MissingPermissions
import typing
from COG.botDatabase import Database
import re


intents = discord.Intents.default()
intents.message_content = True
intents.presences = True



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
        userstatus = interaction.guild.get_member(user.id).status
        embed = discord.Embed(title=f"User Info about {user}")
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_author(name=f'Authored by {interaction.user}', icon_url=interaction.user.avatar.url)
        embed.set_footer(text=f'Discord @ {user}')
        embed.add_field(name='UserID', value=user.id, inline=True)
        embed.add_field(name='Current status', value=userstatus, inline=True)
        embed.add_field(name='Server Join', value=user.joined_at.strftime("%B %d %Y"), inline=True)
        embed.add_field(name='Account age', value=user.created_at.strftime("%B %d %Y"), inline=True)
        await interaction.response.send_message(embed=embed)
    
    # Purge Messages indiscriminately in a channel
    @app_commands.command(
        name="purgemsg",
        description="A command that deletes a specified message",
    )
    @app_commands.describe(
        amount="Amount of messages you want purged"
    )
    @app_commands.describe(
        reason='The Reason'
    )

    async def purge_command(self, interaction: discord.Interaction, amount: int, reason: typing.Optional[str]):
        self.channel = interaction.channel
        await interaction.response.send_message('Attempting to purge messages!', ephemeral=True)
        dltMsgAmount = await self.channel.purge(limit=amount, reason=reason)
        print('Trying to save Purgemsg to log #db')
        # try:
        # await Database.modAction(guildID=discord.Guild.id, modID=interaction.user.id, action=f'Deleted {amount} messages in {interaction.channel}')
        # except:
        #    print('Failed to send data to #db') 
        await interaction.followup.send(f'Deleted {len(dltMsgAmount)} Messages!', ephemeral=True)
    

    # Ban command and stuff
    @app_commands.command(name='ban', description='ban a user')
    @app_commands.describe(user='User you are banning')
    @app_commands.describe(reason='Reason the user is getting banned')
    @app_commands.describe(dltmsg='Deletes the users messages x days back')
    @has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, user: Member, reason: typing.Optional[str], dltmsg: typing.Optional[int]):
        try:
            await user.ban(reason=reason,delete_message_days=dltmsg)
            await interaction.response.send_message(f'User {user} has been banned with the reason: \n "{reason}"')
        except Exception as e:
            print(e)
            await interaction.response.send_message(f'Cannot ban user, {e}') 

    # unban command and stuff
    @app_commands.command(name='unban', description='unban a user')
    @app_commands.describe(user='User you are unbanning')
    @app_commands.describe(reason='Reason the user is getting unbanned')
    @has_permissions(administrator = True)
    async def unban(self, interaction: discord.Interaction, user: Member, reason: typing.Optional[str]):
        try:
            await user.ban(reason=reason)
            await interaction.response.send_message(f'User {user} has been unbanned with the reason: \n "{reason}"')
        except Exception as e:
            print(e)
            await interaction.response.send_message(f'Cannot unban user, {e}') 

    # kick command and stuff
    @app_commands.command(name='kick', description='kick a user')
    @app_commands.describe(user='User you are kicking')
    @app_commands.describe(reason='Reason the user is getting kick')
    @has_permissions(kick_members = True)
    async def  kick(self, interaction: discord.Interaction, user: Member, reason: typing.Optional[str]):
        try:
            await user.kick(reason=reason)
            await interaction.response.send_message(f'User {user} has been kicked with the reason: \n "{reason}"')
        except Exception as e:
            print(e)
            await interaction.response.send_message(f'Cannot kick user, {e}') 
    
    
    # Timeout command
    @app_commands.command(name='timeout', description='timeout a user')
    @app_commands.describe(user='User you are timing out',
                            time='Length of time is: d=Days | h=Hours | m=Minutes | s=Seconds',
                            reason='Reason the user is getting timed out')
    async def mute(self, interaction: discord.Interaction, 
                   user: Member, 
                   reason: typing.Optional[str], 
                   time: typing.Optional[str]): 
        now = datetime.datetime.now()
        if time == None or "":
            duration = datetime.timedelta(days=1)
        # Using regex, find all the times the letters [dhms] are used
        matches = re.findall(r'(\d+)([dhms])',time)
        # Open empty var
        total_seconds = 0
        # Manipulate the var to return an amount of seconds
        if matches:
            for value, unit in matches:
                if unit == 'd':
                    total_seconds += int(value) * 24 * 3600
                elif unit == 'h':
                    total_seconds += int(value) * 3600
                elif unit == 'm':
                    total_seconds += int(value) * 60
                elif unit == 's':
                    total_seconds += int(value)
            # Convert the var to seconds
            duration = datetime.timedelta(seconds=total_seconds)
            # Timeout user using the timedelta str
            await user.timeout(duration, reason=reason)
            # Create unix timestamp for userfriendly-ness  
            unix_timestamp = int((now + duration).timestamp())
            # Send msg informing mod that the action has been taken
            await interaction.response.send_message(f'{user} has been timed out until the <t:{unix_timestamp}> for {reason}')
            print(f'User input was {time}')
            
async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
    # await bot.add_cog('treeCMD') # only to remove class