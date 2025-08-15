import os
import discord #type:ignore
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv #type:ignore

load_dotenv()
APP_ID = int(os.getenv("BOT_APPLICATION_ID")) 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="sha", intents=intents, application_id=APP_ID)

bot.afkdb = sqlite3.connect("../database/general/afk.db")
bot.afkcursor = bot.afkdb.cursor()

bot.afkcursor.execute("""
    CREATE TABLE IF NOT EXISTS afk_users (
        user_id INTEGER PRIMARY KEY,
        reason TEXT,
        since TEXT,
        nickname TEXT
    )
""")
bot.afkcursor.execute("""
    CREATE TABLE IF NOT EXISTS afk_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mentioner_id INTEGER,
        timestamp INTEGER,
        content TEXT
    )
""")
bot.afkdb.commit()

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
