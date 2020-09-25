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


def get_title(url):
    doc = pq(requests.get(url).content)
    title = doc("head title").text()
    if title == "":
        title = doc("body title").text()
        if title == "":
            title = "Untitled page"
    return title


def create_embed(results, start, end):
    embed = discord.Embed(
        title="Google Searches",
        description="Here are your results",
        color=discord.Color.blue(),
    )
    embed.set_thumbnail(
        url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53"
        + "/Google_%22G%22_Logo.svg/235px-Google_%22G%22_Logo.svg.png"
    )

    for link, title in results[start:end]:
        embed.add_field(name=title, value=link, inline=False)
    return embed


class GoogleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ggl(self, ctx, *, query):
        """Takes in desired search and prints top result"""
        results = [
            (i, get_title(i))
            for i in search(
                query, tld="com", lang="en", num=1, start=0, stop=1, pause=2.0
            )
        ]
        await ctx.send(embed=create_embed(results, 0, 1))

    @commands.command()
    async def ggl10(self, ctx, *, query):
        """Takes in desired search and prints top ten results"""

        results = [
            (i, get_title(i))
            for i in search(
                query, tld="com", lang="en", num=10, start=0, stop=10, pause=2.0
            )
        ]

        message = await ctx.send(embed=create_embed(results, 0, 5))

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
                    await message.edit(embed=create_embed(results, 5, 10))
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "▶️" and not status:
                    status = True
                    await message.edit(embed=create_embed(results, 0, 5))
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break


def setup(bot):
    bot.add_cog(GoogleCog(bot))
