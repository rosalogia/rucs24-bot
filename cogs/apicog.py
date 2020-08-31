from discord.ext import commands
import requests
import json

class ApiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        """Says hi"""
        return
    
    @commands.command()
    async def open(self, ctx, index):
        """Takes in course section index and outputs whether the section is open or closed"""

        #Request URL to retrieve indexes of all open sections currently
        open_sections_url = "https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=NB"

        #Try catch in case the api call fails
        try:
            #I load the text from requests call into a list called open_sections
            #open_sections now contains indexes of all open sections
            open_sections = json.loads(requests.get(open_sections_url).text)
        except Exception as e:
            #If something went wrong, output API error and exit function
            await ctx.send("API Error, sorry!")
            print(e)
            return
        
        #Check if index entered is in open sections, output the proper statement
        if index in open_sections:
            await ctx.send(f"Section {index} is currently open!")
        else:
            await ctx.send(f"Section {index} is currently closed!")


def setup(bot):
    bot.add_cog(ApiCog(bot))