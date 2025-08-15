import sqlite3
import datetime
import discord
from profanity_check import predict, predict_prob

class AFK_Handler():
    def __init__(self, interaction, reason, pingwatch):
        self.interaction = interaction
        self.reason = reason
        self.pingwatch = pingwatch
        self.conn = sqlite3.connect("../../databse/general/afk.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS afk_users (
                user_id INTEGER PRIMARY KEY,
                reason TEXT,
                since TEXT
            )
        """)
        self.conn.commit()

    async def run(self):
        name = self.interaction.user.name
        print(f"{name} name fetched.")

        message = ""

        if self.pingwatch.value == "On":
            print("Ping Watch is turned on.")
            guild = self.interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                self.interaction.user: discord.PermissionOverwrite(view_channel=True)
            }
            channel = await guild.create_text_channel("ping-watch", overwrites=overwrites)
            await channel.send(f"{self.interaction.user.mention} this is now the channel to track all your pings while you are AFK.")
            message = f"You are now AFK with ping watch enabled. Reason: {self.reason}"
        else:
            message = f"You are now AFK. Reason: {self.reason}"
        
        await self.interaction.user.edit(nick=f"[AFK] {name}")
        await self.interaction.response.send_message(message, ephemeral=True)

if __name__ == "__main__":
    predict("type shit")

