from discord.ext import commands
import discord
import json
import requests


class LogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_cache = {}

        with open("config.json", "r") as f:
            config_dict = json.load(f)
            try:
                self.log_channel_id = config_dict["logChannel"]
            except KeyError:
                self.log_channel_id = None
                print(
                    "Remember to either disable the log cog or",
                    "set a log channel with !setlogchannel <channel id>"
                )

        with open("config.json", "r") as f:
            config_dict = json.load(f)
            try:
                self.imgur_client_id = config_dict["imgurClientId"]
            except KeyError:
                print("No imgur client id found. Images won't be logged.")

    @commands.command()
    @commands.has_role("Bot Commander")
    async def setlogchannel(self, ctx, channel_id):
        """Enter the id of the channel you want to set the log channel to"""
        log_channel = await self.bot.fetch_channel(channel_id)

        if log_channel == None:
            await ctx.send("Invalid channel!")
            return

        with open("config.json", "r") as f:
            config_dict = json.load(f)
            config_dict["logChannel"] = channel_id

        with open("config.json", "w") as f:
            json.dump(config_dict, f)

        self.log_channel_id = channel_id
        await ctx.send(f"Log channel updated to {log_channel.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Store all sent images in a temporarily available list"""
        for attachment in message.attachments:
            headers = {"Authorization": f"Client-ID {self.imgur_client_id}"}
            payload = {"image": attachment.url}

            imgur_request = requests.post(
                "https://api.imgur.com/3/image",
                headers=headers,
                data=payload
            )

            self.image_cache[message.id] = imgur_request.json()["data"]["link"]

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        log_channel = await self.bot.fetch_channel(self.log_channel_id)

        embed = discord.Embed(
            title="Message Deletion",
            description=f"{message.author.name} in <#{message.channel.id}>",
            color=0xFF0000
        )

        embed.add_field(
            name="Message Content",
            value=message.content if message.content else "Empty message",
            inline=False,
        )

        if message.id in self.image_cache.keys():
            embed.add_field(
                name="Attached Image",
                value=self.image_cache[message.id],
                inline=False
            )

        embed.set_thumbnail(url=str(message.author.avatar_url))

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author == self.bot.user:
            return

        if message_before.content == message_after.content:
            return

        log_channel = await self.bot.fetch_channel(self.log_channel_id)

        embed = discord.Embed(
            title="Message Edit",
            description=f"{message_before.author.name} in <#{message_before.channel.id}>",
            color=0xFF0000
        )
        embed.add_field(name="Before", value=message_before.content, inline=False)
        embed.add_field(name="After", value=message_after.content, inline=True)
        embed.set_thumbnail(url=str(message_before.author.avatar_url))

        await log_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(LogCog(bot))
