import discord
import os
import logging
import sqlite3
from discord.ext import commands


class DbSqlite(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        # Configure cog logging
        logger_name = os.getenv('COG_DBSQLITE_LOGGER_NAME')
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename=f"{logger_name}", encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

        sqlite_db = os.getenv('SQLITE_DB')
        self.bot = bot
        self.db = sqlite3.connect(sqlite_db)
        self.db_cursor = self.db.cursor()
        self.db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            discriminator TEXT
        )
        """)

    @commands.command()
    async def whoami(self, ctx: commands.Context):
        self.db_cursor.execute("SELECT * FROM users WHERE id=?", (ctx.author.id,))
        response = self.db_cursor.fetchone()
        if not response:
            self.db_cursor.execute("INSERT INTO users VALUES (?,?,?)",
                                   (ctx.author.id, ctx.author.name, ctx.author.discriminator,))
            self.db.commit()
            response = self.db_cursor.fetchone()

        uid, name, discriminator = response
        await ctx.send("<@{}>, you are {}#{}.".format(uid, name, discriminator))


def setup(bot: commands.Bot):
    bot.add_cog(DbSqlite(bot))
