import requests
import discord
from discord.ext import commands


class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        """Tells you a joke; Respond to setup with ? to hear the punchline"""
        r = requests.get("https://official-joke-api.appspot.com/random_joke")
        apidata = r.json()
        await ctx.send(apidata["setup"])

        def check(message):
            return message.author.id == ctx.author.id

        response = await self.bot.wait_for("message", check=check)
        if response.content == "?":
            await ctx.send(apidata["punchline"])


def setup(bot):
    bot.add_cog(JokeCog(bot))
