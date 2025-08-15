import discord
from discord import app_commands
from discord.ext import commands
from . import afk_handler

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="afk", description="Go AFK!")
    @app_commands.describe(reason="Your reason for AFK.")
    async def afk(self, interaction: discord.Interaction, reason:str):
        handler = afk_handler.AFK_Handler(interaction, reason, self.bot.afkdb, self.bot.afkcursor)
        await handler.run()
    
    @app_commands.command(name="reason", description="Check reason for AFK.")
    @app_commands.describe(target="the user that is AFK.")
    async def reason(self, interaction: discord.Interaction, target: discord.Member):
        handler = afk_handler.AFK_Listener(self.bot.afkdb, self.bot.afkcursor)
        answer = handler.is_afk(target.id)
        if answer:
            print("work1")
            await interaction.response.send_message(f"User is AFK with reason:\n\n'{answer[0]}'", ephemeral=True)
        else:
            await interaction.response.send_message("User is currently not AFK.", ephemeral=True)
    
    @app_commands.command(name="logs", description="Check mention logs while you were AFK.")
    async def logs(self, interaction: discord.Interaction):
        handler = afk_handler.AFK_Listener(self.bot.afkdb, self.bot.afkcursor)
        msg = handler.get_logs(interaction.user.id)
        await interaction.response.send_message(msg, ephemeral=True)


class GeneralListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        handler = afk_handler.AFK_Listener(self.bot.afkdb, self.bot.afkcursor)
        if handler.is_afk(message.author.id):
            times = handler.get_time(message.author.id)
            if times:
                await handler.remove_afk(message.author)
                msg = f"Welcome Back {message.author.mention}. You were afk for "
                if times[0] > 0:
                    msg += f"{round(times[0])} days, "
                if times[1] > 0:
                    msg += f"{round(times[1])} hours, "
                if times[2] > 0:
                    msg += f"{round(times[2])} minutes, "
                msg += f"{round(times[3])} seconds."

                await message.reply(msg)

        for user in message.mentions:
            if handler.is_afk(user.id):
                handler.log_mention(user.id, message)
                times = handler.get_time(user.id)
                if times:
                    msg = f"User was AFK "
                    if times[0] > 0:
                        msg += f"{round(times[0])} days, "
                    if times[1] > 0:
                        msg += f"{round(times[1])} hours, "
                    if times[2] > 0:
                        msg += f"{round(times[2])} minutes, "
                    msg += f"{round(times[3])} seconds ago.\nDo `/reason` for reason."

                    await message.reply(msg)


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
    await bot.add_cog(GeneralListeners(bot))
