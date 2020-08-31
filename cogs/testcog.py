import discord
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Prints message to terminal when bot is ready"""
        #Uses client.user to output name and id of bot
        print(f'Logged on as {self.bot.user}')


    @commands.command()
    async def echo(self, ctx, *args):
        """Takes in space separated arguments and outputs those same arguments"""
        #Uses join command to space separate args, no matter how many there are
        await ctx.send(' '.join(args))

    
    @commands.command()
    async def help(self, ctx):
        """Displays information about all the commands in the bot"""
        #Create an embed with information on each command
        embed = discord.Embed(title="Help", description="RUCS24 Commands", color=0xff0000)
        embed.add_field(name="!echo", value="Params: Any Phrase\nDescription: Repeats your phrase word for word", inline=False)
        embed.add_field(name="!open", value="Params: Section Index\nDescription: Tells you whether a given course section is open or closed currently", inline=False)
        embed.add_field(name="!tictactoe", value="Params: None\nDescription: Starts a game of tictactoe with the player", inline=False)

        #Send the embed
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TestCog(bot))