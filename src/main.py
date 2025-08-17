import os
import discord #type:ignore
import make_tables
from discord.ext import commands
from dotenv import load_dotenv #type:ignore
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),      
    port=os.getenv("DB_PORT"),     
    user=os.getenv("DB_USER"),     
    password=os.getenv("DB_PW"),  
    database=os.getenv("DB_AFKDB")  
)

if conn.is_connected():
    print("Connected to MySQL Database.")

APP_ID = int(os.getenv("BOT_APPLICATION_ID")) 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="sha", intents=intents, application_id=APP_ID)
cursor = conn.cursor()
bot.afkcursor = cursor
bot.afkdb = conn

make_tables.create(bot)

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
        try:
            await bot.start(TOKEN)
        finally:
            bot.afkcursor.close()
            bot.afkdb.close()

import asyncio
asyncio.run(main())
