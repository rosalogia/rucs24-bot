import discord
from discord.ext import commands


class TimeConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def convert(cls, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)

            except KeyError:
                raise commands.BadArgument(f"{value} is an invalid time key!")

            except ValueError:
                raise commands.BadArgument(f"{key} is not a number")

        return round(time)


def setup(bot):
    bot.add_cog(TimeConverter(bot))
    å
