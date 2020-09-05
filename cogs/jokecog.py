import requests
import discord
from discord.ext import commands


class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        # Code will go here
        return


def setup(bot):
    bot.add_cog(JokeCog(bot))
