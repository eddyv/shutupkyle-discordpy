import discord
import os
import logging

from discord import Message, RawReactionActionEvent, Activity, ActivityType
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
logger_name = os.getenv('MAIN_LOGGER_NAME')

# setup logging
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f"{logger_name}", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix=PREFIX)

initial_extensions = ['cogs.DbSqlite']

'''
Called after login has been successful
'''


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    logger.info(f'I\'m currently in the following servers: {bot.guilds}')
    logger.info(discord.opus.is_loaded())
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="Shutup Kyle: The Movie"))


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


"""
Make the bot react using the same emote.
"""


@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    logger.info(f'on_raw_reaction called')
    logger.info(str(payload))
    emoji = payload.emoji
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    await message.add_reaction(emoji)


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


@bot.command(name='load', help='Loads an extension')
async def load(extension_name: str):
    """Loads an extension."""
    try:
        print(f'Loading extension {extension_name}.')
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(name='unload', help='Unloads an extension')
async def unload(extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            print(f'Load extension {extension}.')
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')

bot.run(TOKEN)
