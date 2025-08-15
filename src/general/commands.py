import discord
from discord import app_commands
from discord.ext import commands
import afk_handler as afk

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="afk", description="Go AFK! Optionally watch for pings.")
    @app_commands.describe(reason="Your reason for AFK. English letters only.", pingwatch="Turn on to track pings.")
    @app_commands.choices(pingwatch=[
        app_commands.Choice(name = "On", value = "On"), 
        app_commands.Choice(name = "Off", value = "Off")
        ])
    async def afk(self, interaction: discord.Interaction, reason:str, pingwatch:app_commands.Choice[str]):
        afk.AFK_Handler(interaction, reason, pingwatch)
        afk.run()


class GeneralListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "hello" in message.content.lower():
            await message.channel.send(f"Hello, {message.author.mention}!")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
    await bot.add_cog(GeneralListeners(bot))
