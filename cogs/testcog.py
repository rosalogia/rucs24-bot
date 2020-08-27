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


def setup(bot):
    bot.add_cog(TestCog(bot))