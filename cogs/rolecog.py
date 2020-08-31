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
        self.bot = bot
        self._roles_config = read_from_config('roles')
        self._selector_channel_id = self._roles_config['selectorChannel']
        self._listeners = self._roles_config['listeners']


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        selector_channel = self.bot.get_channel(self._selector_channel_id)
        if selector_channel is None:
            print(f"Error: No valid selector channel was specified.") 
            return
        
        message = await selector_channel.fetch_message(payload.message_id)
        guild = selector_channel.guild
        member = payload.member
        
        valid_emoji_lists = map(lambda listener: listener.keys(), self._listeners.values())
        valid_emojis = [item for sublist in valid_emoji_lists for item in sublist]
        
        if str(payload.emoji) in valid_emojis:
            corresponding_role = guild.get_role(self._listeners[str(message.id)][str(payload.emoji)])
            if corresponding_role not in member.roles:
                await member.add_roles(corresponding_role)
        else:
            await message.remove_reaction(payload.emoji, member)
        return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        selector_channel = self.bot.get_channel(self._selector_channel_id)
        if selector_channel is None:
            print(f"Error: No valid selector channel was specified.") 
            return
        
        message = await selector_channel.fetch_message(payload.message_id)
        guild = selector_channel.guild
        member = guild.get_member(payload.user_id)
       
        # Creating a list of lists of valid emojis, then flattening it to create a single-dimensional list
        valid_emoji_lists = map(lambda listener: listener.keys(), self._listeners.values())
        valid_emojis = [item for sublist in valid_emoji_lists for item in sublist]
        
        if str(payload.emoji) in valid_emojis:
            corresponding_role = guild.get_role(self._listeners[str(message.id)][str(payload.emoji)])
            if corresponding_role in member.roles:
                await member.remove_roles(corresponding_role)
        return

def setup(bot):
    bot.add_cog(RoleCog(bot))
