# RUCS24-bot

A discord bot for the Rutgers Class of 2024 Computer Science server

## Build Instructions

1. Create a copy of the file called `starter_config.json` and rename it to `config.json`
1. Replace YOUR_TOKEN in `config.json` with your bot account's token.
```json
{
    "botToken" : YOUR_TOKEN,
    …
}
```
1. Run `pip install -r requirements.txt`
1. Run `python main.py`

## "Features"

RUCS24-Bot has certain cogs that won't work and may throw errors
until the environment is properly configured for them to run. This
usually means including some information in the config file.

If you're having trouble and are confused, consider reading the comments
in the cog you want to enable until we find a better way to document
each one's usage instructions.

In order to enable a feature, simply include it in the "features" array 
in `config.json`. Here are the presently available features:

* "api": Connects to the Rutgers WebReg API to see if a course section is open
* "tictactoe": Allows the user to play tictactoe with the bot
* "connectfour": Allows the user to play Connect 4 with the bot
* "github": Allows users to register a GitHub account with the bot in order to track their contributions to any specified repositories. Note that this feature must be enabled for "exp" to work.
* "exp": Awards EXP to users for contributing to certain repositories, and rewards them with roles for reaching certain levels
* "react": A more robust implementation of "role"
* "joke": The bot tells a user a joke when a command is called
* "minecraft": Allows the user to whitelist themselves in a minecraft server by registering their username with the bot
* "fun": Provides arbitrary and entertaining commands
* "latex": Provides commands for generating and sending images of compiled LaTeX code to the chat
* "log": Provides functionality for the logging of deleted or edited messages and images
* "covid": Returns the confirmed, death, and test covid count for the state
* "whois": Provides details about a user by mentioning them
