import requests
import urllib.parse
import io
import discord
from discord.ext import commands


class LatexCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latex(self, ctx, *, arguments):
        """Parses LaTeX and returns an image with the formatted result"""
        latex = urllib.parse.quote(arguments)
        req_url = (
            "https://latex.codecogs.com/png.latex?\\dpi{300}&space;\\bg_black&space;%s"
            % (latex)
        )
        r = requests.get(req_url)
        b = io.BytesIO(r.content)
        # b = io.BytesIO(svg2png(url=req_url, dpi=300, background_color='white'))
        await ctx.send(file=discord.File(b, "LaTeX.png"))


def setup(bot):
    bot.add_cog(LatexCog(bot))
