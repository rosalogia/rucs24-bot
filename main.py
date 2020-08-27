from configuration import config
import discord
from discord.ext import commands
import requests
import json

client = commands.Bot(command_prefix='!', help_command=None)


@client.event
async def on_ready():
    """Prints message to terminal when bot is ready"""
    #Uses client.user to output name and id of bot
    print(f'Logged on as {client.user}')


@client.command()
async def echo(ctx, *args):
    """Takes in space separated arguments and outputs those same arguments"""
    #Uses join command to space separate args, no matter how many there are
    await ctx.send(' '.join(args))


@client.command()
async def open(ctx, index):
    """Takes in course section index and outputs whether the section is open or closed"""

    #Request URL to retrieve indexes of all open sections currently
    open_sections_url = "https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=NB"

    #Try catch in case the api call fails
    try:
        #I load the text from requests call into a list called open_sections
        #open_sections now contains indexes of all open sections
        open_sections = json.loads(requests.get(open_sections_url).text)
    except:
        #If something went wrong, output API error and exit function
        await ctx.send("API Error, sorry!")
        return
    
    #Check if index entered is in open sections, output the proper statement
    if index in open_sections:
        await ctx.send(f"Section {index} is currently open!")
    else:
        await ctx.send(f"Section {index} is currently closed!")


#Run the bot using the token in config.json
client.run(config["botToken"])
