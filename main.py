from configuration import config
from discord.ext import commands
from datetime import datetime


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
    "resource",
    "command"
]

# Load extensions specified in features
for feature in features:
    try:
        bot.load_extension(f"cogs.{feature}cog")
    except Exception as e:
        print(f"{bcolors.FAIL}WARN: Cog {feature} failed to load{bcolors.ENDC}")
        with open("log.txt", "a") as log_file:
            current_time = datetime.now().strftime("%H:%M:%S")
            msg = f"[{current_time}] in cog {feature}:\n{e}\n\n"
            log_file.write(msg)

# Run the bot using the token in config.json
bot.run(config["botToken"])
