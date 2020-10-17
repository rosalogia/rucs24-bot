import discord
from discord.ext import commands


class ChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cs"])
    async def channelstats(self, ctx):

        channel = ctx.channel
        embed = discord.Embed(
            title=f"Stats for {channel.name}", description=channel.category.name
        )
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel ID", value=channel.id, inline=False)
        embed.add_field(
            name="Channel Topic",
            value=channel.topic if channel.topic else "No Topic",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(
            name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        embed.add_field(
            name="Channel Creation Time", value=channel.created_at, inline=False
        )
        embed.add_field(
            name="Channel Permissions Synced",
            value=channel.permissions_synced,
            inline=False,
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ChannelCog(bot))
