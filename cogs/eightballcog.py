import discord
from discord.ext import commands
import random


class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8Ball", "Random8"])
    async def _8Ball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


def setup(bot):
    bot.add_cog(EightBall(bot))
