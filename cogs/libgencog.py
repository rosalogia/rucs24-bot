from libgen_api import LibgenSearch
import discord
from discord.ext import commands


class LibgenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def libgen(self, ctx, *args):
        """Enter a title search query and it will respond with libgen entries"""

        # Collect their query and search for it
        search_query = " ".join(args)

        s = LibgenSearch()
        results = s.search_title(search_query)

        # Truncate to at most 6 results
        results = results[:6]

        # If no results, tell them their book isn't libgenable
        if len(results) == 0:
            await ctx.send("Sorry! Your book isn't libgenable :(")
            return

        # Set up discord embed
        embed = discord.Embed(
            title="Search Results", description=f"Query: {search_query}", color=0xFF0000
        )

        # Add all the info of each search result to the embed in its own field
        for num in range(1, len(results) + 1):
            info_str = ""
            info_str += f'Author: {results[num-1]["Author"]}\n'
            info_str += f'Title: {results[num-1]["Title"]}\n'
            info_str += f'Publisher: {results[num-1]["Publisher"]}\n'
            info_str += f'Year: {results[num-1]["Year"]}\n'
            info_str += f'Extension: {results[num-1]["Extension"]}\n'
            info_str += "Download Links:\n"
            info_str += f'[1]({results[num-1]["Mirror_1"]}) [2]({results[num-1]["Mirror_2"]}) [3]({results[num-1]["Mirror_3"]}) [4]({results[num-1]["Mirror_4"]}) [5]({results[num-1]["Mirror_5"]})'

            embed.add_field(name=f"Result {num}", value=info_str)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LibgenCog(bot))
