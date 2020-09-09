# RUCS24-bot

A discord bot for the Rutgers Class of 2024 Computer Science server

## Build Instructions

1. Create a file called `config.json` and include the following contents, but be sure to replace YOUR_TOKEN with your bot account's token
```json
{
    "botToken" : YOUR_TOKEN
}
```
2. Run `pip install -r requirements.txt`
3. Run `python main.py`

## Using Disabled Cogs

Some cogs are disabled by default because in order to use them,
you're going to have to adjust your `config.json` file in ways we
can't necessarily predict you'll want to.

You can look at `example_config.json` to see how you might structure
your `config.json` file in order to enable the modules you want to use.
If you're having trouble and are confused, consider reading the comments
in the cog you want to enable until we find a better way to document
each one's usage instructions.