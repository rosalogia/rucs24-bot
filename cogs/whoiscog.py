import discord
from discord.ext import commands
from datetime import datetime, timezone


class WhoisCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member):
        """Provides details about a user by mentioning them"""

        embed = discord.Embed(
            title="User Info - " + member.display_name, color=member.color
        )
        current_time = datetime.now().strftime("Today at %I:%M %p")
        roles = member.roles

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.author} at {current_time}",
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
