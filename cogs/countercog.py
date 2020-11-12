import discord
from discord.ext import commands
import json
from .utils import create_ine, get_data


class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        create_ine("data/counters.json")

    @commands.command()
    @commands.has_role("Bot Commander")
    async def setcounter(self, ctx, name, count="0"):
        """Sets a counter with the specified name and optional starting count, default is zero"""
        with get_data("counters") as counters:
            counters[name] = count

        await ctx.send(f"Counter {name} updated to {count}")

    @commands.command()
    @commands.has_role("Bot Commander")
    async def removecounter(self, ctx, name):
        """Removes a counter given counter name"""
        with get_data("counters") as counters:
            try:
                counters.pop(name)
            except KeyError:
                await ctx.send("No counter with that name!")
                return

        await ctx.send(f"There is now no counter for {name}")

    @commands.command()
    async def listcounters(self, ctx):
        """Lists counters"""
        with get_data("counters", update=False) as counters:
            desc = "\n".join([k for k in counters.keys()])

        embed = discord.Embed(title="Counters", description=desc, color=0xFF0000)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Bot Commander")
    async def increment(self, ctx, name, amt="1"):
        """Increments specified counter by a specified amount, default is 1"""
        with get_data("counters") as counters:
            try:
                counters[name] = str(int(counters[name]) + int(amt))
            except KeyError:
                await ctx.send("No counter with that name!")
                return

        await ctx.send(
            f"Counter {name} updated from {int(counters[name]) - int(amt)} to {counters[name]}"
        )

    @commands.command()
    @commands.has_role("Bot Commander")
    async def decrement(self, ctx, name, amt="1"):
        """Decrements specified counter by a specified amount, default is 1"""
        with get_data("counters") as counters:
            try:
                counters[name] = str(int(counters[name]) - int(amt))
            except KeyError:
                await ctx.send("No counter with that name!")
                return

        await ctx.send(
            f"Counter {name} updated from {int(counters[name]) + int(amt)} to {counters[name]}"
        )

    @commands.command()
    async def counter(self, ctx, name):
        """Checks the value of a counter"""
        with get_data("counters") as counters:
            try:
                await ctx.send(counters[name])
            except KeyError:
                await ctx.send("There is no counter with that name!")


def setup(bot):
    bot.add_cog(CounterCog(bot))
