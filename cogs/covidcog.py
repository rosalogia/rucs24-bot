import discord
from discord.ext import commands
import requests


def embedCreator(data):
    """
    Creates the embedded message for the covid-19 stats
    """
    state = data["state"]
    todayCases = data["todayCases"]
    todayDeaths = data["todayDeaths"]
    embed_title = f":world_map: Covid Stats in {state} :world_map:"
    embed = discord.Embed(title=embed_title, color=0x8D0000)
    embed.description = f"Statistics for Covid-19 in {state}"
    embed.add_field(
        name=f"Total {state} Cases",
        value="Total Cases: {:,} {}".format(
            data["cases"], f"(+{todayCases})" if todayCases != 0 else ""
        ),
        inline=True,
    )
    embed.add_field(
        name=f"Total {state} Deaths",
        value="Total Deaths: {:,} {}".format(
            data["deaths"], f"(+{todayDeaths})" if todayDeaths != 0 else ""
        ),
        inline=True,
    )
    embed.add_field(
        name=f"Total {state} Tests",
        value="Total Tests: {:,}".format(data["tests"]),
        inline=True,
    )
    embed.set_footer(text="Data from corona.lmao.ninja")
    return embed


class CovidCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def covid(self, ctx, *state_name):
        """
        Request Covid Data per State
        """
        state_name = " ".join(state_name).title()
        api_data = requests.get("https://corona.lmao.ninja/v2/states").json()

        try:
            returning_data, *_ = [
                state_data
                for state_data in api_data
                if state_data["state"] == state_name
            ]
        except ValueError:
            await ctx.send("State not found")
            return

        await ctx.send(embed=embedCreator(returning_data))


def setup(bot):
    bot.add_cog(CovidCog(bot))
