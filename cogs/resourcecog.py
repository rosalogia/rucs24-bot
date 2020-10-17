from discord.ext import commands
import discord
import json
from discord.utils import get
from .utils import create_ine, get_config, update_config


def save_resources(resource_dict):
    with open("data/resources.json", "w") as f:
        json.dump(resource_dict, f)


def load_resources():
    with open("data/resources.json", "r") as f:
        return json.load(f)


def create_embed(msgauth, name, link, desc, tags):
    embed = discord.Embed(
        title="Resource Suggestion",
        description="Suggestion made by " + msgauth,
        color=0x66FF99,
    )

    embed.add_field(name="Resource Name", value=name, inline=False)

    embed.add_field(name="Link", value=link, inline=False)

    embed.add_field(name="Description", value=desc, inline=False)

    embed.add_field(name="Tags", value=tags, inline=False)
    return embed


def edit_embed(rinfo):
    return create_embed(
        rinfo["msgauth"], rinfo["name"], rinfo["link"], rinfo["desc"], rinfo["tags"]
    )


async def send_resource(rsc_channel, msg):
    await msg.delete()
    resource_dict = load_resources()
    rinfo = resource_dict[str(msg.id)]
    rscembed = discord.Embed(
        title=rinfo["name"], description=rinfo["desc"], color=0x66FF99
    )
    rscembed.add_field(name="Link", value=rinfo["link"], inline=True)
    rscembed.add_field(name="Tags", value=rinfo["tags"], inline=True)
    rscembed.set_footer(text="Submitted by " + rinfo["msgauth"])
    await rsc_channel.send(embed=rscembed)
    del resource_dict[str(msg.id)]
    save_resources(resource_dict)


class ResourceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        create_ine("data/resources.json")

        cfg = get_config()
        try:
            self.resource_channel_id = cfg["resourceChannel"]
        except KeyError:
            self.resource_channel_id = None
            print("Remember to !setresourcechannel")
        try:
            self.review_channel_id = cfg["reviewChannel"]
        except KeyError:
            self.review_channel_id = None
            print("Remember to !setreviewchannel")

    @commands.command()
    @commands.has_role("Bot Commander")
    async def setresourcechannel(self, ctx, channel_id):
        """Enter ID of channel to set as resource channel"""
        rsc_channel = await self.bot.fetch_channel(channel_id)

        if rsc_channel is None:
            await ctx.send("Invalid channel id")
            return

        cfg = get_config()
        cfg["resourceChannel"] = channel_id
        update_config(cfg)

        self.resource_channel_id = channel_id
        await ctx.send(f"{rsc_channel.name} has been set as resources channel")

    @commands.command()
    @commands.has_role("Bot Commander")
    async def setreviewchannel(self, ctx, channel_id):
        """Enter ID of channel to set as review channel"""
        rvw_channel = await self.bot.fetch_channel(channel_id)

        if rvw_channel is None:
            await ctx.send("Invalid channel id")
            return

        cfg = get_config()
        cfg["reviewChannel"] = channel_id
        update_config(cfg)

        self.review_channel_id = channel_id
        await ctx.send(f"{rvw_channel.name} has been set as review channel")

    @commands.command()
    async def suggestresource(self, ctx, rscname, rsclink, rscdesc, *, rsctags):
        """Suggest a resource with the name, link, description (in quotes), and tags"""
        rvw_channel = await self.bot.fetch_channel(self.review_channel_id)
        message = await rvw_channel.send(
            embed=create_embed(
                ctx.message.author.name, rscname, rsclink, rscdesc, rsctags
            )
        )
        await message.add_reaction("✔️")
        await message.add_reaction("❎")
        resource_dict = load_resources()
        await ctx.message.add_reaction("✔️")

        resource_dict[str(message.id)] = {}
        rinfo = resource_dict[str(message.id)]
        rinfo["name"] = rscname
        rinfo["link"] = rsclink
        rinfo["desc"] = rscdesc
        rinfo["tags"] = rsctags
        rinfo["msgauth"] = str(ctx.message.author.name)
        save_resources(resource_dict)

    @commands.command()
    @commands.has_role("Bot Commander")
    async def rscedit(self, ctx, msg_id, editedmsg):
        """Edit a resource description by inputting the id of the message and the new description"""
        resource_dict = load_resources()
        try:
            resource_dict[str(msg_id)]["desc"] = editedmsg
        except KeyError:
            await ctx.send("That is not a valid ID")
        channel = self.bot.get_channel(int(self.review_channel_id))
        message = await channel.fetch_message(int(msg_id))
        await message.edit(embed=edit_embed(resource_dict[str(msg_id)]))
        save_resources(resource_dict)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.channel_id) == self.review_channel_id:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.emoji.name == "✔️":
                reaction = get(message.reactions, emoji=payload.emoji.name)
                if reaction.count > 1:
                    rsc_channel = await self.bot.fetch_channel(self.resource_channel_id)
                    await send_resource(rsc_channel, message)
            if payload.emoji.name == "❎":
                reaction = get(message.reactions, emoji=payload.emoji.name)
                if reaction.count > 1:
                    await message.delete()
                    resource_dict = load_resources()
                    del resource_dict[str(message.id)]
                    save_resources(resource_dict)


def setup(bot):
    bot.add_cog(ResourceCog(bot))
