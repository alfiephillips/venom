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

    @commands.command(name="ping", help="Test the bots current ping!")
    async def ping(self, ctx):
        embed = self.em(title="My current ping!", description=f"{round(self.bot.latency * 1000, 1)}ms")
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))