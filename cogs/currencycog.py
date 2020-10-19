import requests
import discord
from discord.ext import commands


class CurrencyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cconvert(self, ctx, base, target, amount: float = 1):
        """Converts between currencies"""

        # To do: round the output (number of decimal places differs by currency)

        try:
            payload = {"symbols": target, "base": base}
            r = requests.get("https://api.exchangeratesapi.io/latest", params=payload)
            apidata = r.json()
            result = float(apidata["rates"][target]) * amount

            embed = discord.Embed(title="Currency Conversion")
            embed.add_field(name=f"From {base}:", value=f"```{amount}```")
            embed.add_field(name=f"To {target}:", value=f"```{result}```")
            embed.set_footer(text="Powered by https://exchangeratesapi.io/")

            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Invalid currency code(s)")


def setup(bot):
    bot.add_cog(CurrencyCog(bot))
