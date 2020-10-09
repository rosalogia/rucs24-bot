import discord
from discord.ext import commands
import json


class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Bot Commander")
    async def setcommand(self, ctx, name, *args):
        """Adds a custom command with the first word as command and rest as response"""

        # Retrieve commands, add command, dump new dict, send msg
        with open("data/commands.json", "r") as f:
            commands = json.load(f)

        commands[name] = " ".join(args)

        with open("data/commands.json", "w") as f:
            json.dump(commands, f)

        await ctx.send(f"Command {name} updated!")

    @commands.command()
    @commands.has_role("Bot Commander")
    async def removecommand(self, ctx, name):
        """Removes a custom command with the given name"""

        # Get dict, remove given command, and write new dict
        with open("data/commands.json", "r") as f:
            commands = json.load(f)

        try:
            commands.pop(name)
        except:
            await ctx.send("No command with that name!")
            return

        with open("data/commands.json", "w") as f:
            json.dump(commands, f)

        await ctx.send(f"There is now no command for {name}")

    @commands.command()
    async def listcommands(self, ctx):
        """Lists custom commands"""

        with open("data/commands.json", "r") as f:
            commands = json.load(f)

        desc = "\n".join([k for k in commands.keys()])

        embed = discord.Embed(title="Custom Commands", description=desc, color=0xFF0000)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Check for custom commands on every message"""

        # Get commands, if the message is in commands.keys() send the command
        with open("data/commands.json", "r") as f:
            commands = json.load(f)

        if msg.content in commands.keys() and msg.author.id != self.bot.user.id:
            await msg.channel.send(commands[msg.content])


def setup(bot):
    bot.add_cog(CommandCog(bot))
