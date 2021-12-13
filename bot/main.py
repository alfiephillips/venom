import asyncio
import discord
import logging
import time
import datetime

from discord.ext import commands
from discord.ext.commands.errors import *

from aiohttp import ClientSession
from config import TOKEN, MONGO_URI, SERVER_ID
from pymongo import MongoClient

from helpers import check_env
from cogs.utils.context import Context

cogs = [
    "cogs.commands"
]

class Venom(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', ('Venom!', 'venom!', 'V!', 'v!')),
                         case_insensitive=True,
                         **kwargs)
        self.session = ClientSession(loop=self.loop)
        self.start_date = datetime.datetime.utcnow()
        self.start_time = time.time()
        self.clean_text = commands.clean_content(escape_markdown=True, fix_channel_mentions=True)

        logging.basicConfig(level=logging.INFO)

        "Listening for events"

    async def on_connect(self):
        """
        Connecting to the discord server.
        """

        check_env()
        
        end = time.time()

        print(f"Bot has connected: {round(end - self.start_time, 2)} seconds.")

        self.start_time = end

    async def on_ready(self):
        """
        On bot load.
        """

        print(f'Successfully logged in as {self.user}\nSharded to {len(self.guilds)} guilds')
        self.guild = self.get_guild(SERVER_ID)
        await self.change_presence(activity=discord.Game(name="Scalping the internet..."))

        for extension in cogs:
            self.load_extension(extension)
        
        end = time.time()

        print(f"All extensions have loaded: {round(end - self.start_time, 2)} seconds.")

    async def on_message(self, message):
        """
        Every message sent by a user.
        """

        await self.wait_until_ready()

        if message.author.bot or not message.guild:
            return None

        print(f"{message.channel} - {message.author}: {message.clean_content}")

        await self.process_commands(message)

    async def process_commands(self, message):
        """
        Process all commands with certain prefix.
        """
        if message.author.bot:
            return 

        ctx = await self.get_context(message=message)

        if ctx.command is None:
            return 

        

        return await self.invoke(ctx)

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message=message, cls=cls or Context)


    @classmethod
    async def setup(cls, **kwargs):
        bot = cls()
        try:
            await bot.start(TOKEN, **kwargs)
        except KeyboardInterrupt:
            print("Bot stopping...")
            await bot.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Venom.setup())