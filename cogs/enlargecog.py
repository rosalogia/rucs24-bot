import discord
from discord.ext import commands


class EnlargeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["Avatar"])
    async def avatar(self, ctx, user: discord.Member):
        """Returns enlarged avatar of @ed user"""
        embed = discord.Embed(color=discord.Color(0xFFFF), title=str(user))

        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def emoji(self, ctx, emoji: discord.Emoji):
        """Returns enlarged custom emoji"""
        await ctx.send(emoji.url)


def setup(bot):
    bot.add_cog(EnlargeCog(bot))
