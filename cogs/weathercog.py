from discord.ext import commands
import requests
from .utils import get_config


class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # This line in the constructor is required

    @commands.command()
    async def test(self, ctx):  # the ctx parameter is short for 'context'
        """Sends a message that indicates that the command has worked"""
        await ctx.send("Test succeeded. Command is operational")

    @commands.command()
    async def weather(self, ctx):
        config = get_config()
        payload = {
            "q": "New Brunswick,US-NJ,US",
            "appid": config["WeatherAPIKey"],
            "units": "imperial",
        }
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather", params=payload
        )
        response_content = response.json()
        temp = response_content["main"]["temp"]
        await ctx.send(f"The weather in New Brunswick is {temp}")

    @commands.command()
    async def testinput(self, ctx):
        def check(message):
            return message.author.id == ctx.author.id

        await ctx.send("Enter city name")
        cityName = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter state code")
        stateCode = await self.bot.wait_for("message", check=check)
        await ctx.send("Enter country code")
        countryCode = await self.bot.wait_for("message", check=check)
        config = get_config()
        payload = {
            "q": [cityName.content, stateCode.content, countryCode.content],
            "appid": config["WeatherAPIKey"],
            "units": "imperial",
        }
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather", params=payload
        )
        response_content = response.json()
        temp = response_content["main"]["temp"]
        await ctx.send(f"The weather in {cityName.content} is {temp}")


def setup(bot):
    bot.add_cog(WeatherCog(bot))
