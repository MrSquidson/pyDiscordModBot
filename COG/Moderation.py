import discord
from discord import app_commands
from discord.ext import commands


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

   
    # @app_commands.describe(
    #     reason="The reason why you're purging messages"
    # )  

    async def delete_command(self, interaction: discord.Interaction, amount: int, reason: str):
        self.channel = interaction.channel
        await interaction.response.send_message('Attempting to purge messages!', ephemeral=True)
        dltMsgAmount = await self.channel.purge(limit=amount, reason=reason)
        await interaction.followup.send(f'Deleted {len(dltMsgAmount)} Messages!', ephemeral=True)




async def setup(bot):
    await bot.add_cog(treeCMD(bot))
    # await bot.add_cog('treeCMD') # only to remove class