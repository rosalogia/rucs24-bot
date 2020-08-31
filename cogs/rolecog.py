from discord.ext import commands
import json

# I have no idea how to effectively move this function to any file other than the one I need it in
def read_from_config(key):
    """Looks for a particular item within the config file

    Args:
        key: the key for which a value in the config file should be found

    Returns:
        The value corresponding to the key"""

    with open('./config.json') as config_file:
        try:
            return json.load(config_file)[key]
        except KeyError:
            return None

class RoleCog(commands.Cog):
    def __init__(self, bot):
        """Initialise the bot and draw important values from the configuration file"""

        self.bot = bot
        self._roles_config = read_from_config('roles')
        self._selector_channel_id = self._roles_config['selectorChannel']
        self._listeners = self._roles_config['listeners']

    async def add_remove_role(self, payload, add):
        """Add or remove a role in response to a reaction to a specified message in a specified channel

        Args:
            payload: A discord.RawReactionEvent object representing the reaction or reaction removal
            add: A boolean denoting whether or not the event being fired is a reaction being added"""

        selector_channel = self.bot.get_channel(self._selector_channel_id)
        if selector_channel is None:
            print(f"Error: No valid selector channel was specified.") 
            return
        
        message = await selector_channel.fetch_message(payload.message_id)
        guild = selector_channel.guild
        member = guild.get_member(payload.user_id)

        # Grabbing a list of lists of valid emojis from the config file and then flattening it into one single list
        # Learn more about the map and lambda syntax here: https://medium.com/better-programming/lambda-map-and-filter-in-python-4935f248593
        valid_emoji_lists = map(lambda listener: listener.keys(), self._listeners.values())
        valid_emojis = [item for sublist in valid_emoji_lists for item in sublist]
        
        if str(payload.emoji) in valid_emojis:
            corresponding_role = guild.get_role(self._listeners[str(message.id)][str(payload.emoji)])
            if corresponding_role not in member.roles and add:
                await member.add_roles(corresponding_role)
            elif corresponding_role in member.roles and not add:
                await member.remove_roles(corresponding_role)
        elif add: # In the case that someone reacted with an emoji that doesn't correspond to a role
            await message.remove_reaction(payload.emoji, member)
        return


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.add_remove_role(payload, True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.add_remove_role(payload, False)

def setup(bot):
    bot.add_cog(RoleCog(bot))
