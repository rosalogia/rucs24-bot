import discord
from discord.ext import commands
from googlesearch import search
import asyncio
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

# class TitleParser(HTMLParser):
#     def __init__(self):
#         HTMLParser.__init__(self)
#         self.match = False
#         self.title = ''

#     def handle_starttag(self, tag, attributes):
#         self.match = True if tag == 'title' else False

#     def handle_data(self, data):
#         if self.match:
#             self.title = data
#             self.match = False


class GoogleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ggl(self, ctx, *, query):
        result = []
        for i in search(query, tld="com", lang="en", num=1, start=0, stop=1, pause=2.0):
            result.append(str(i))
        print(result[0])

        if pq(requests.get(result[0]).content)("head title").text() == "":
            title = "Title Not Found"
        else:
            title = pq(requests.get(result[0]).content)("head title").text()
        embed = discord.Embed(
            title="Google Searches",
            description="Here is your result",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(
            url="https://www.freepnglogos.com/uploads/google-logo-png/google-logo-png-suite-everything-you-need-know-about-google-newest-0.png"
        )
        embed.add_field(name=title, value=result[0], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def ggl10(self, ctx, *, query):
        """Takes in desired search and number of results to output given Google Searches"""

        def get_title(url):
            return pq(requests.get(url).content)("head title").text()

        results = []
        for i in search(
            query, tld="com", lang="en", num=10, start=0, stop=10, pause=2.0
        ):
            if get_title(i) == "":
                title = "Title Not Found"
            else:
                title = get_title(i)
            results.append((i, title))

        def add_result(start, end):
            embed = discord.Embed(
                title="Google Searches",
                description="Here are your results",
                color=discord.Color.blue(),
            )
            embed.set_thumbnail(
                url="https://www.freepnglogos.com/uploads/google-logo-png/google-logo-png-suite-everything-you-need-know-about-google-newest-0.png"
            )

            for link, title in results[start:end]:
                embed.add_field(name=title, value=link, inline=False)
            return embed

        message = await ctx.send(embed=add_result(0, 5))

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "▶️"

        await message.add_reaction("▶️")
        status = True
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60, check=check
                )
                if str(reaction.emoji) == "▶️" and status:
                    status = False
                    await message.edit(embed=add_result(5, 10))
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "▶️" and not status:
                    status = True
                    await message.edit(embed=add_result(0, 5))
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break


def setup(bot):
    bot.add_cog(GoogleCog(bot))
