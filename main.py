from configuration import config
import discord
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned, help_command=None)

@client.event
async def on_ready():
    print(f'Logged on as {self.user}')

@client.command()
async def test(ctx, content):
    await ctx.send(content)

client.run(config["botToken"])
