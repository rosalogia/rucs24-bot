from discord.ext import commands
from unit_converter.converter import convert, converts


class ConversionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # This line in the constructor is required

    @commands.command()
    async def convert(
        self, ctx, inputunit, outputunit
    ):  # the ctx parameter is short for 'context'
        """type your input and output units"""
        save = convert(inputunit, outputunit)

        await ctx.send(
            "You are converting from "
            + inputunit
            + " to "
            + str(save)
            + " "
            + outputunit
        )


def setup(bot):
    bot.add_cog(ConversionCog(bot))
