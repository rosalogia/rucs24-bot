from configuration import config
from discord.ext import commands

# Initialize bot with prefix '!'
bot = commands.Bot(command_prefix="!", help_command=None)

# Load extensions from cogs folder
bot.load_extension("cogs.corecog")
bot.load_extension("cogs.apicog")
bot.load_extension("cogs.tictactoecog")
bot.load_extension("cogs.connectfourcog")
# bot.load_extension("cogs.rolecog")
# bot.load_extension("cogs.githubcog")
# bot.load_extension("cogs.expcog")
bot.load_extension("cogs.reactcog")
bot.load_extension("cogs.jokecog")
bot.load_extension("cogs.commandcog")
# bot.load_extension("cogs.minecraftcog")

# Run the bot using the token in config.json
bot.run(config["botToken"])
