from configuration import config
import discord
from discord.ext import commands

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

client.run(config["botToken"])
