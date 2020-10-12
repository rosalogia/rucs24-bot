import discord
from discord.ext import commands


class AvatarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["Avatar"])
    async def avatar(self, ctx, user: discord.Member):

        embed = discord.Embed(color=discord.Color(0xFFFF), title=f"{user}")

        embed.set_image(url=f"{user.avatar_url}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AvatarCog(bot))
