import requests
import discord
from discord.ext import commands
from discord.ext import commands
from discord.ext.commands import check
from discord import voice_client


class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def aumute(self, ctx):
        for member in list(bot.get_channel("461333256944615424").members):
            member[1].setMute(True)


def setup(bot):
    bot.add_cog(MuteCog(bot))
