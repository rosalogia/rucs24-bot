import requests
import discord
from discord.ext import commands


class AffirmationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def affirmation(self, ctx):
        """Tells you a positive affirmation"""
        r = requests.get("https://www.affirmations.dev/")
        apidata = r.json()
        await ctx.send(apidata["affirmation"])


def setup(bot):
    bot.add_cog(AffirmationCog(bot))
