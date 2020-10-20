import discord
import os
from discord.ext import commands
from discord.utils import get
import youtube_dl
from youtube_search import YoutubeSearch
import validators


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["J", "jo"])
    async def join(self, ctx):
        """Have the bot join the voice channel to which you're currently connected"""
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        # Work around for currently existing issue wherein
        # music will not play upon first connection
        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command(pass_context=True, aliases=["L", "le"])
    async def leave(self, ctx):
        """Have the bot leave the voice channel to which it's currently connected"""
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("Error: no voice channel to leave")

    @commands.command(pass_context=True, aliases=["p", "pl"])
    async def play(self, ctx, url: str):
        """Have the bot play the audio from a provided youtube link.
        If no valid url is provided, the bot will interpret the input
        as a search term and find the first result for the given input.

        If a search term contains more than one word, make sure to wrap
        the search term in quotes.

        Usage: `!play <youtube_link | search_term>`
        """
        if not validators.url(url):
            url = (
                "https://youtube.com"
                + YoutubeSearch(url, max_results=1).videos[0]["url_suffix"]
            )

        song_there = os.path.isfile("./data/song.mp3")
        try:
            if song_there:
                os.remove("./data/song.mp3")
        except PermissionError:
            print(
                "Error: unable to remove old song file. Do you have permission to do this?"
            )
            await ctx.send("Permission error. Please contact an administrator.")
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
            ],
            "outtmpl": "./data/%(title)s.%(ext)s",
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir("./data/"):
            if file.endswith("mp3"):
                name = " ".join(file.split(".")[:-1])
                await self.bot.change_presence(
                    activity=discord.Activity(
                        name=name, type=discord.ActivityType.listening
                    )
                )
                os.rename(f"./data/{file}", "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        await ctx.send(f"Playing: {name}")

    @commands.command(pass_context=True, aliases=["pa", "pau"])
    async def pause(self, ctx):
        """Pause currently playing music"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Music Paused")
        else:
            await ctx.send("Music is not playing, pause failure")

    @commands.command(pass_context=True, aliases=["re", "resum"])
    async def resume(self, ctx):
        """Resume playback of music that has been paused"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Music Resumed")
        else:
            await ctx.send("Music is not playing, resume failure")

    @commands.command(pass_context=True, aliases=["st", "stp"])
    async def stop(self, ctx):
        """Stop the playback of music that is currently playing"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Music Stopped")
        else:
            await ctx.send("Music is not playing, stop failure")


def setup(bot):
    bot.add_cog(MusicCog(bot))
