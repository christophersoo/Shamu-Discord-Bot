import os
import discord #type:ignore
from discord.ext import commands #type:ignore
from dotenv import load_dotenv #type:ignore

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="sh", intents=intents)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot.run(TOKEN)
