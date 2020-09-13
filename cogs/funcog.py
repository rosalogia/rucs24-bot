import discord
from discord.ext import commands
from random import choice


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randomize(self, ctx, *args):
        """Randomizes capitalization of inputted string"""
        await ctx.send("".join([choice([c.upper(), c.lower()]) for c in " ".join(args)]))


def setup(bot):
    bot.add_cog(FunCog(bot))
