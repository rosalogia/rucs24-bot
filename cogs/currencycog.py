import requests
import discord
from discord.ext import commands


class CurrencyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cconvert(self, ctx, *args):
        """Converts between currencies"""

        # To do:
        # 1. make it output a fancy embed thing
        # 2. round the output (number of decimal places differs by currency)

        try:
            initial_value = float(args[2]) if len(args) > 2 else 1
            payload = {"symbols": args[1], "base": args[0]}
            r = requests.get("https://api.exchangeratesapi.io/latest", params=payload)
            apidata = r.json()
            await ctx.send(float(apidata["rates"][args[1]])*initial_value)
        except IndexError:
            await ctx.send("Invalid syntax")
        except KeyError:
            await ctx.send("Invalid currency code(s)")


def setup(bot):
    bot.add_cog(CurrencyCog(bot))
