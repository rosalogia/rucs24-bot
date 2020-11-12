import discord
import pytz
from discord.ext import commands
from datetime import datetime, timezone


class WhoisCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        """Provides details about a user by mentioning them"""

        if not member:
            member = ctx.message.author
        embed = discord.Embed(
            title=f"User Info - {member}",
            color=member.color,
        )
        eastern = pytz.timezone("US/Eastern")
        east_time = datetime.now(eastern)
        current_time = east_time.strftime("%I:%M %p")
        roles = member.roles
        roles.reverse()

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.message.author} | {current_time}",
            icon_url=ctx.author.avatar_url,
        )

        embed.add_field(name="Tag", value=member.mention)
        embed.add_field(name="ID", value=member.id)

        embed.add_field(
            name="Joined",
            value=member.joined_at.strftime("%a, %b %d, %Y at %I:%M:%S %p"),
            inline=False,
        )
        embed.add_field(
            name="Registered",
            value=member.created_at.astimezone(timezone.utc).strftime(
                "%a, %b %d, %Y at %I:%M:%S %p"
            ),
        )
        embed.add_field(
            name="Roles", value=" ".join([role.mention for role in roles]), inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(WhoisCog(bot))
