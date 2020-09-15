import discord
from discord.ext import commands


class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Prints message to terminal when bot is ready"""
        # Uses client.user to output name and id of bot
        print(f"Logged on as {self.bot.user}")

    @commands.command()
    async def echo(self, ctx, *args):
        """Takes in space separated arguments and outputs those same arguments"""
        # Uses join command to space separate args, no matter how many there are
        await ctx.send(" ".join(args))

    @commands.command()
    async def help(self, ctx):
        """Displays information about all the commands in the bot"""

        # Create the embed, set up the title and description, as well as scarlet red color
        embed = discord.Embed(
            title="Help", description="RUCS24 Commands", color=0xFF0000
        )

        # Stores cog name and maps to all the functions
        cogs_dict = {}

        # Go through each command, access its name and docstring, add to embed
        for func in self.bot.walk_commands():
            # Adds the function to cogs_dict based on its cog
            try:
                cogs_dict[func.cog_name].append((func.name, func.help))
            except:
                cogs_dict[func.cog_name] = [(func.name, func.help)]

        # Create the cog, add all the commands, and send the embed
        for cog in cogs_dict.keys():
            embed = discord.Embed(title=cog, description="Help", color=0xFF0000)

            for command in cogs_dict[cog]:
                embed.add_field(name="!" + command[0], value=command[1], inline=False)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CoreCog(bot))
