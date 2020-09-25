import urllib.parse
import re
import discord
from discord.ext import commands

cols = {
    "transparent": "",
    "white": "\\bg_white&space;",
    "black": "\\bg_black&space;",
    "red": "\\bg_red&space;",
    "green": "\\bg_green&space;",
    "blue": "\\bg_blue&space;",
}


class LatexCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latex(self, ctx, *, arguments):
        """Parses LaTeX and returns an image with the formatted result"""
        await self.send_latex(ctx, arguments)

    @commands.command()
    async def latexcol(self, ctx, *, arguments):
        """Parses LaTeX and returns an image with the formatted result using a specified color"""
        res = re.search("\\s", arguments)
        if res == None:
            error = "Error: no color provided"
            error += "\nValid colors: %s" % (
                ", ".join("`" + x + "`" for x in cols.keys())
            )
            await ctx.send(error)
            return
        split_ind = res.start()
        col = arguments[:split_ind].lower()
        inp = arguments[split_ind:].strip()
        await self.send_latex(ctx, inp, col)

    async def send_latex(self, ctx, inp, col="black"):
        latex = urllib.parse.quote(inp)
        try:
            colcode = cols[col]
        except KeyError:
            error = "Error: Invalid color: `%s`" % (col)
            error += "\nValid colors: %s" % (
                ", ".join("`" + x + "`" for x in cols.keys())
            )
            await ctx.send(error)
            return

        req_url = (
            "https://latex.codecogs.com/png.latex?\\dpi{300}&space;%s\\huge&space;%s"
            % (colcode, latex)
        )

        embed = discord.Embed(title="LaTeX output", color=0x0539F5)
        embed.add_field(name="Input:", value="`%s`" % (inp), inline=False)
        embed.set_image(url=req_url)
        embed.set_footer(text="Generated by codecogs.com")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LatexCog(bot))
