import asyncio
import datetime
import discord

from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def em(title, description):
        embed = discord.Embed(title=title, description=description)
        return embed

    @commands.command(name="newlink", help="Create a new link to scalp on either Amazon, ...")
    async def new_link(self, ctx, link):
        pass

def setup(bot):
    bot.add_cog(Commands(bot))