import platform
import logging
import discord
from discord.ext import commands, tasks


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverstats(self, ctx):
        pythonVersion = platform.python_version()
        dpyversion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        await ctx.send(
            f"So im in {serverCount} guilds with a total of {memberCount} members. :smiley:\nIm running python {pythonVersion} and discord.py {dpyversion}"
        )


def setup(bot):
    bot.add_cog(StatsCog(bot))
