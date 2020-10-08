from configuration import config
from discord.ext import commands


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Initialize bot with prefix '!'
bot = commands.Bot(command_prefix="!", help_command=None)

features = [
    "api",
    "core",
    "tictactoe",
    "connectfour",
    "role",
    "github",
    "exp",
    "react",
    "joke",
    "minecraft",
    "fun",
    "codeexecution",
    "latex",
    "google",
    "log",
    "covid",
    "affirmation",
]

# Load extensions specified in features
for feature in features:
    try:
        bot.load_extension(f"cogs.{feature}cog")
    except Exception:
        print(f"{bcolors.FAIL}WARN: Cog {feature} failed to load{bcolors.ENDC}")

# Run the bot using the token in config.json
bot.run(config["botToken"])
