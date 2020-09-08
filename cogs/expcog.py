from discord.ext import commands, tasks
import requests
import polling
from github import Github
import json
from datetime import datetime, timedelta
from functools import reduce


# Load the registration data ahead of time
with open("data/github_registrations.json", "r") as registration_file:
    registrations = json.load(registration_file)

with open("data/contribution_exp.json", "r") as contribution_exp_file:
    contribution_exp = json.load(contribution_exp_file)


class ExpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            self.github_session = Github(
                    config["github"]["user"],
                    config["github"]["password"]
                    )
            self.repository = self.github_session.get_repo(
                    config["github"]["repository"]
                    )

        self.event_cache = []

        self.update.start()

    def score_event(self, event):
        score_table = {
                "CommitCommentEvent" : 0,
                "CreateEvent" : 0,
                "DeleteEvent" : 0,
                "ForkEvent" : 20,
                "GollumEvent" : 0,
                "IssueCommentEvent" : 2.5,
                "IssuesEvent" : 5,
                "MemberEvent" : 0,
                "PublicEvent" : 0,
                "PullRequestReviewCommentEvent" : 2.5,
                "PushEvent" : 0,
                "ReleaseEvent" : 0,
                "SponsorshipEvent" : 0,
                "WatchEvent" : 2.5
                }

        # Handle exceptions to the table

        if event.type == "IssueCommentEvent" and event.payload["action"] != "created":
            return 0
        elif event.type == "IssuesEvent" and event.payload["action"] != "opened":
            return 0
        elif event.type == "PullRequestEvent" and event.payload["action"] != "opened":
            return 0
        elif event.type == "PullRequestEvent":
            return event.payload["pull_request"]["additions"] * 0.15
        elif event.type == "PushEvent":
            commits = list(map(
                lambda commit: self.repository.get_commit(sha=commit["sha"]),
                event.payload["commits"]
                ))
            return reduce((lambda x, y: x + y),
                    map(
                        lambda commit: commit.stats.additions,
                        commits
                        )) * 0.15
        else:
            return score_table[event.type]


    @tasks.loop(seconds=15.0)
    async def update(self):
        # print(f"Checking repository {self.repository.name} for events")
        recent_events = list(filter(
                lambda event: event.created_at > datetime.utcnow() - timedelta(minutes=5) and event.id not in self.event_cache,
                self.repository.get_events()))

        self.event_cache += list(map(lambda event: event.id, recent_events))
        # print(f"Recent events cached. Current event cache: {self.event_cache}")

        # print("Found recent events: ")
        # for event in recent_events:
        #     print(f"Type: {event.type} ; Actor: {event.actor.login} ; Created at: {event.created_at}")


        # print(f"Valid users: {list(registrations.values())}")

        for user in registrations.keys():
            user_events = list(filter(
                    lambda event: event.actor.login == registrations[user],
                    recent_events 
                    ))

            # print(f"Found events {list(user_events)} for user {registrations[user]}")
            try:
                gained_exp = reduce(lambda x, y: x + y, map(self.score_event, user_events))
            except TypeError:
                gained_exp = 0

            # print(f"{registrations[user]} earned {gained_exp} exp")
            contribution_exp[user] += gained_exp

        with open("data/contribution_exp.json", "w+") as contribution_exp_file:
            json.dump(contribution_exp, contribution_exp_file)

    @commands.command()
    async def exp(self, ctx):
        """Check how much exp you currently have"""
        if str(ctx.author.id) not in registrations.keys():
            await ctx.send("Your GitHub account is not registered with RUCS24.")
        else:
            await ctx.send(f"You have {contribution_exp[str(ctx.author.id)]} exp points")

def setup(bot):
    bot.add_cog(ExpCog(bot))
