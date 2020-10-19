import json
import requests
import discord
from discord.ext import commands
import urllib


class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, lang_from, lang_to, *args):
        """Input a 2 letter code for lang_from and lang_to, and then the text to be translated"""
        input_str = " ".join(args)
        safe_input_str = urllib.parse.quote(input_str, safe="")
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={lang_from}&tl={lang_to}&dt=t&q={safe_input_str}"
        req = requests.get(url)
        try:
            translated_text = req.json()[0][0][0]
        except:
            await ctx.send("Invalid input or output language!")
            return
        embed = discord.Embed(title="Google Translate", color=0x4B8CF5)
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Google_Translate_logo.svg/500px-Google_Translate_logo.svg.png"
        )
        embed.add_field(name="Input Text", value=input_str)
        embed.add_field(name="Output Text", value=translated_text, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TranslateCog(bot))
