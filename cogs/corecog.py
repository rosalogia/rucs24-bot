import discord
from discord.ext import commands
import os

class CoreCog(commands.Cog):
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
        
        #Create the embed, set up the title and description, as well as scarlet red color
        embed = discord.Embed(title="Help", description="RUCS24 Commands", color=0xff0000)
        
        #Go through each command, access its name and docstring, add to embed
        for func in self.bot.walk_commands():
            embed.add_field(name='!'+func.name, value=func.help, inline=False)
        
        #Finally, send the embed
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(CoreCog(bot))