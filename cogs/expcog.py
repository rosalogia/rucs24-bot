from discord import Embed
from discord.ext import commands, tasks
from github import Github
import json
from datetime import datetime, timedelta
from functools import reduce
from math import floor, sqrt
from .utils import create_ine, get_config, update_config


class ExpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        create_ine("data/contribution_exp.json")
        create_ine("data/github_registrations.json")

        # Only load configuration that has to do with this cog
        self.config = get_config()["github"]
        self.github_session = Github(self.config["token"])

        # If we ever have more than one RUCS24
        # repository, we can store them all
        # in a list, and we'll get exp no
        # matter which one we're contributing to
        self.repositories = [
            self.github_session.get_repo(repo) for repo in self.config["repositories"]
        ]

        self.reward_roles = self.config["reward_roles"]

        self.event_cache = []

        self.update.start()

    def level(self, exp):
        """A user's contributor level as a function of their exp"""
        return floor((sqrt(625 + 20 * exp) - 25) / 10)

    def exp(self, level):
        """The amount of EXP required to achieve a certain level"""
        return 5 * level * (level + 5)

    async def award_roles(self, guild_id, user_id):
        """Give the specified reward roles to the user
        if applicable

        Args:
            guild_id (string):  the id of the guild to which
                                the roles belong

            user_id (string):   the user whose roles are
                                being updated"""

        with open("data/github_registrations.json", "r") as registration_file:
            registrations = json.load(registration_file)

        with open("data/contribution_exp.json", "r") as contribution_exp_file:
            contribution_exp = json.load(contribution_exp_file)

        current_guild = self.bot.get_guild(int(guild_id))
        member = current_guild.get_member(int(user_id))

        if self.reward_roles == {}:
            return
        else:
            level_requirements = sorted(list(self.reward_roles.keys()))
            level_requirements.reverse()

            role_assigned = False

            for role_level in level_requirements:
                role_object = current_guild.get_role(self.reward_roles[role_level])
                if (
                    self.level(contribution_exp[user_id]) >= int(role_level)
                    and not role_assigned
                ):
                    if role_object in member.roles:
                        return
                    else:
                        await member.add_roles(role_object)

                        await member.add_roles(role_object)
                        role_assigned = True
                elif role_assigned and role_object in member.roles:
                    await member.remove_roles(role_object)
                else:
                    pass

    def statistics_embed(self, channel_id, author_id):
        """Create and return an embed containing
        contribution statistics for the given member

        Args:
            channel_id (string):    the id of the channel
                                    in which the embed will be sent

            author_id (string):     the id of the member to whom
                                    the embed pertains

        Returns:
            discord.Embed:  an embed containing the contribution
                            statistics for the given member

        """

        with open("data/github_registrations.json", "r") as registration_file:
            registrations = json.load(registration_file)

        with open("data/contribution_exp.json", "r") as contribution_exp_file:
            contribution_exp = json.load(contribution_exp_file)

        # Getting a member object can be ugly since
        # we need the Guild object first. This is
        # actually the only reason this method needs
        # access to the channel_id, so let me know
        # if you have a better idea
        author = self.bot.get_channel(int(channel_id)).guild.get_member(int(author_id))
        author_login = registrations[author_id]
        author_exp = contribution_exp[author_id]
        stats_embed = Embed(
            title=f"{author.nick if author.nick else author}'s Contribution Profile",
            description="Want to be rewarded for your contributions to RUCS24? Register your GitHub account with !register",
            color=0xFF0000,
        )
        stats_embed.set_thumbnail(url=f"https://github.com/{author_login}.png")
        stats_embed.add_field(
            name="GitHub",
            value=f"[{author_login}](https://github.com/{author_login})",
            inline=True,
        )
        stats_embed.add_field(
            name="Level", value=f"{self.level(author_exp)}", inline=True
        )
        stats_embed.add_field(
            name="Current EXP", value=str(floor(author_exp)), inline=True
        )
        stats_embed.add_field(
            name="EXP till Next Level",
            value=str(floor(self.exp(self.level(author_exp) + 1) - author_exp)),
            inline=True,
        )

        return stats_embed

    def score_event(self, event):
        """Assign an EXP value to a given GitHub event

        Args:
            event (github.Event.Event): the repository event being scored

        Returns:
            int: the EXP value assigned to the event, potentially based on lines added"""

        # Default score values are stored in config
        score_table = self.config["score_table"]

        # Configure exceptions to the score table
        # E.g. Only issue creations and issue comments award EXP
        if event.type == "IssueCommentEvent" and event.payload["action"] != "created":
            return 0
        elif event.type == "IssuesEvent" and event.payload["action"] != "opened":
            return 0
        elif event.type == "PullRequestEvent" and event.payload["action"] != "opened":
            return 0
        elif event.type == "PullRequestEvent":
            # 15% of the amnt of lines added becomes EXP
            return event.payload["pull_request"]["additions"] * 0.15
        elif event.type == "PushEvent":
            # Same rule as for PRs, the logic is just more complicated for commits
            commits = list(
                filter(
                    # Only the repository owner can push, so these must belong to
                    # the repository owner. Reconfigure if collaborating directly.
                    lambda commit: commit.author.login == event.repo.owner.login
                    # Merge commits don't count, since they're not your code
                    and "Merge" not in commit.commit.message,
                    map(
                        lambda commit: event.repo.get_commit(sha=commit["sha"]),
                        event.payload["commits"],
                    ),
                )
            )

            try:
                return (
                    reduce(  # We all wish Python was better at this
                        (lambda x, y: x + y),
                        map(lambda commit: commit.stats.additions, commits),
                    )
                    * 0.15
                )
            # reduce throws a TypeError if the list
            # its passed is empty or doesn't exist
            except TypeError:
                return 0
        else:
            return score_table[event.type]

    @tasks.loop(seconds=15.0)
    async def update(self):
        """Look for new events that have occurred within
        the last five minutes every 15 seconds. Registered
        events will be cached until the bot is restarted.
        However, if the bot is restarted 5 minutes after
        the event is registered, it won't be registered
        again."""

        with open("data/github_registrations.json", "r") as registration_file:
            registrations = json.load(registration_file)

        with open("data/contribution_exp.json", "r") as contribution_exp_file:
            contribution_exp = json.load(contribution_exp_file)

        raw_event_list = reduce(
            lambda x, y: x + y, map(lambda repo: repo.get_events(), self.repositories)
        )

        recent_events = list(
            filter(
                lambda event: event.created_at
                > datetime.utcnow() - timedelta(minutes=5)
                and event.id not in self.event_cache,
                raw_event_list,
            )
        )

        self.event_cache += list(map(lambda event: event.id, recent_events))

        # Some debugging stuff if things aren't working on your end:

        # print(f"Recent events cached. Current event cache: {self.event_cache}")

        # print("Found recent events: ")
        # for event in recent_events:
        #     print(f"Type: {event.type} ; Actor: {event.actor.login} ; Created at: {event.created_at}")

        # print(f"Valid users: {list(registrations.values())}")

        for user in registrations.keys():
            user_events = list(
                filter(
                    lambda event: event.actor.login == registrations[user],
                    recent_events,
                )
            )

            # print(f"Found events {list(user_events)} for user {registrations[user]}")

            try:
                gained_exp = sum(map(self.score_event, user_events))

            except TypeError:
                gained_exp = 0

            try:
                # If you set an update channel, the bot will
                # send a message their whenever someone levels up
                update_channel = self.bot.get_channel(self.config["update_channel"])
            except KeyError:
                update_channel = None

            # print(f"{registrations[user]} earned {gained_exp} exp")
            contribution_exp[user] += gained_exp

            # print(f"Update channel is none: {update_channel is None}")

            with open("data/contribution_exp.json", "w+") as contribution_exp_file:
                json.dump(contribution_exp, contribution_exp_file)

            if update_channel:
                current_level = self.level(contribution_exp[user])

                if self.level(contribution_exp[user] + gained_exp) > current_level:
                    current_level = self.level(contribution_exp[user] + gained_exp)

                    await update_channel.send(
                        f"<@{user}> **has levelled up!**",
                        embed=self.statistics_embed(str(update_channel.id), user),
                    )

                # Unless we set a single server in config
                # we can only award roles if an update channel
                # is specified
                await self.award_roles(str(update_channel.guild.id), user)

    @update.before_loop
    async def before_update(self):
        """Just to make sure the event grabber
        doesn't run until the bot is ready.
        Otherwise it won't be able to use any
        methods under self.bot"""

        await self.bot.wait_until_ready()

    @commands.command()
    async def stats(self, ctx, *user):
        """View information about your or someone else's contribution level"""

        with open("data/github_registrations.json", "r") as registration_file:
            registrations = json.load(registration_file)

        author = (
            ctx.message.mentions[0]
            if len(user) > 0 and len(ctx.message.mentions) > 0
            else ctx.author
        )
        if str(author.id) not in registrations.keys():
            await ctx.send(
                f"{author.mention}'s GitHub account is not registered with RUCS24."
            )
        else:
            stats_embed = self.statistics_embed(str(ctx.channel.id), str(author.id))
            await ctx.send(embed=stats_embed)

    @commands.command()
    async def restore(self, ctx, user):
        """Restore EXP for a user that the bot
        wasn't able to grab recent events for"""

        if not ctx.author.permissions_in(ctx.channel).administrator:
            await ctx.send("You cannot use this command.")
        else:
            with open("data/github_registrations.json", "r") as registration_file:
                registrations = json.load(registration_file)

            with open("data/contribution_exp.json", "r") as contribution_exp_file:
                contribution_exp = json.load(contribution_exp_file)

            if user not in registrations.keys():
                await ctx.send("Specified user is not registered.")
            else:
                raw_event_list = reduce(
                    lambda x, y: x + y,
                    map(lambda repo: repo.get_events(), self.repositories),
                )

                self.event_cache += list(map(lambda event: event.id, raw_event_list))

                user_events = list(
                    filter(
                        lambda event: event.actor.login == registrations[user],
                        raw_event_list,
                    )
                )

                try:
                    gained_exp = sum(map(self.score_event, user_events))
                except TypeError:
                    gained_exp = 0

                contribution_exp[user] += gained_exp

                await self.award_roles(str(ctx.channel.guild.id), user)

                with open("data/contribution_exp.json", "w") as contribution_exp_file:
                    json.dump(contribution_exp, contribution_exp_file)


def setup(bot):
    bot.add_cog(ExpCog(bot))
