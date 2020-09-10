import discord
from discord.ext import commands
import json

class DuplicateError(Exception):
    """Exception raised if an already
    existing value is added to a collection
    that prohibits duplicate values"""
    pass

class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json", "r") as config_file:
            config = json.load(config_file)["minecraft"]
            self.whitelist_path = config["whitelist_path"]
            self.confirmation_channel_id = config["confirmation_channel_id"]

    def update_whitelist(self, username, isAddition=True):
        """Update the whitelist file with the given username

        Args:
            username (string): the Minecraft username being added or removed
            isAddition (bool): whether the username is being added or removed"""

        with open(self.whitelist_path, "r") as whitelist_file:
            whitelist = json.load(whitelist_file)

        if isAddition:
            if username in whitelist:
                raise DuplicateError
            else:
                whitelist.append(username)
        else:
            # This might throw a ValueError,
            # but we should handle it later
            whitelist.remove(username)

        with open(self.whitelist_path, "w") as whitelist_file:
            json.dump(whitelist, whitelist_file)

        return

    def update_accountmap(self, user_id, minecraft_username, isAddition=True):
        """Update the locally stored JSON file that contains
        maps a Discord user to a Minecraft username

        Args:
            user_id (int): the user's Discord ID
            minecraft_username (string): the user's Minecraft username
            isAddition (bool): whether or not you're adding or removing a mapping"""

        with open("data/mc_accountmap.json", "r") as accountmap_file:
            accountmap = json.load(accountmap_file)

        if isAddition:
            accountmap[str(user_id)] = minecraft_username
        else:
            # This might throw a KeyError,
            # but again we should handle
            # that later
            del accountmap[str(user_id)]
       
        with open("data/mc_accountmap.json", "w") as accountmap_file:
            json.dump(accountmap, accountmap_file)

        return

    @commands.command()
    async def mcregister(self, ctx, username):
        """Register your Minecraft username with your
        Discord account to be whitelisted on our Minecraft
        server"""

        with open("data/mc_accountmap.json", "r") as accountmap_file:
            accountmap = json.load(accountmap_file)
        
        if ctx.channel.id != self.confirmation_channel_id:
            await ctx.send(
                "This is not the right channel for this command. "
                f"Try again in <#{self.confirmation_channel_id}>"
            )
        elif str(ctx.author.id) in accountmap.keys():
            await ctx.send(
                        f"User {ctx.author.mention} has already "
                        f"registered username {accountmap[str(ctx.author.id)]}"
                    )
        else:
            try:
                self.update_whitelist(username)
            except DuplicateError:
                await ctx.send("You are already registered")
                return

            self.update_accountmap(ctx.author.id, username)

            await ctx.send(f"Whitelisted minecraft user {username}. `!mcunregister` to undo this")

    @commands.command()
    async def mcunregister(self, ctx):
        """Unregister your Minecraft username from your Discord
        account and subsequently be unwhitelisted"""
        try:
            with open("data/mc_accountmap.json", "r") as accountmap_file:
                username = json.load(accountmap_file)[str(ctx.author.id)]
        except KeyError:
            await ctx.send(f"Member {ctx.author.mention} is not registered.")
            return
        try:
            self.update_whitelist(username, isAddition=False)
        except ValueError:
            await ctx.send(f"User {username} not found in whitelist")

        try:
            self.update_accountmap(ctx.author.id, username, isAddition=False)
        except KeyError:
            print(f"Mapping {ctx.author.id} : {username} not in file")

        await ctx.send("Successfully unregistered")


def setup(bot):
    bot.add_cog(MinecraftCog(bot))
