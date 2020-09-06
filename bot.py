import discord
import os
import logging

from discord import Message
from discord.ext.commands import Context
from dotenv import load_dotenv
from discord.ext import commands

import sqlite3

# get env vars
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('PREFIX')
sqliteDB = os.getenv('SQLITE_DB')
logger_name = os.getenv('LOGGER_NAME')

# setup logging
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix=PREFIX)

# db connection
connection = sqlite3.connect(sqliteDB)
cursor = connection.cursor()

'''
Called after login has been successful
'''


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    logger.info(f'I\'m currently in the following servers: {bot.guilds}')
    logger.info(discord.opus.is_loaded())


'''
Called after a message is sent to the server
'''


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    logger.info(message.content)
    # when using on_message it forbids any extra commands from running. using the below causes it to process commands
    await bot.process_commands(message)


"""Below is an example of a Local Error Handler for our command do_repeat"""


@bot.command(name='user', help='Reports with the # of shutups for a particular user')
async def get_user_stats(ctx: Context):
    pass


@bot.command(name='stats', help='Top 10 stats')
async def get_stats(ctx: Context):
    pass


@bot.command(name='shutuptts', help='TTS - Shutup Kyle')
async def send_shutup_tts(ctx: Context):
    await ctx.send("Shut Up Kyle", tts=True)


@bot.command(name='shutupmp4', help='mp4 - Shutup Kyle')
async def send_shutup_mp4(ctx: Context):
    await ctx.send("Shut Up Kyle", tts=True)


@bot.command(name='prune', help='prune <number of messages>')
async def purge(ctx: Context, amount: int):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'Deleted {len(deleted)} message(s)')


bot.run(TOKEN)
