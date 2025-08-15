import os
import discord #type:ignore
from discord.ext import commands
from dotenv import load_dotenv #type:ignore

load_dotenv()
APP_ID = int(os.getenv("BOT_APPLICATION_ID")) 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="sha", intents=intents, application_id=APP_ID)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

async def load():
    await bot.load_extension("general.commands")

async def main():
    async with bot:
        TOKEN = os.getenv("BOT_TOKEN")
        await load()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())