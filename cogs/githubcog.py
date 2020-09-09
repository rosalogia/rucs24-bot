from discord.ext import commands
import requests
import polling
from github import Github
import json


def request_codes():
    """Request device and verification codes from the GitHub OAuth API

    Returns:
        dict: a JSON response containing both codes
    """
    return requests.post(
        "https://github.com/login/device/code",
        # Only request permission to read user information
        {"client_id": "45e2376f056230c072a5", "scope": "read:user"},
        headers={"Accept": "application/json"},
    ).json()


def poll_for_token(codes):
    """Poll the OAuth API for an access token
    Args:
        codes (dict): the JSON response from the API call
                      containing the device and verification codes

    Returns:
        dict:   the JSON response from the API that contains
                either the access_token or an error message
    """

    req = requests.post(
        "https://github.com/login/oauth/access_token",
        {
            "client_id": "45e2376f056230c072a5",
            "device_code": codes["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        },
        headers={"Accept": "application/json"},
    )
    try:
        if req.json()["error"] == "authorization_pending":
            return None
        else:
            return req.json()
    except KeyError:
        return req.json()


# Load the registration data ahead of time
with open("data/github_registrations.json", "r") as registration_file:
    registrations = json.load(registration_file)

with open("data/contribution_exp.json", "r") as contribution_exp_file:
    contribution_exp = json.load(contribution_exp_file)


class GithubCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        """DMs the user with instructions for registering
        their GitHub account with the bot"""

        code_response = request_codes()
        await ctx.author.send(
            "To register your GitHub account with RUCS24-Bot, "
            "go to <https://github.com/login/device> and enter "
            f"the code: {code_response['user_code']}"
        )

        token_response = polling.poll(
            lambda: poll_for_token(code_response), step=10, poll_forever=True
        )

        try:
            user_token = token_response["access_token"]
            auth_session = Github(user_token)
            user_login = auth_session.get_user().login

            await ctx.author.send(
                f"Registered as **{user_login}** on GitHub.\n"
                "**WARNING**: You will need to !unregister and "
                "register again if you change your GitHub username."
            )

            with open("data/github_registrations.json", "w+") as registration_file:
                registrations[str(ctx.author.id)] = auth_session.get_user().login
                json.dump(registrations, registration_file)

            with open("data/contribution_exp.json", "w+") as contribution_exp_file:
                contribution_exp[str(ctx.author.id)] = 0
                json.dump(contribution_exp, contribution_exp_file)

        except KeyError:
            print(f"Error dump: {token_response}")
            await ctx.author.send(
                "There was an issue processing your request. "
                "Please contact an RUCS24 Admin."
            )

    @commands.command()
    async def check_registration(self, ctx):
        """Checks the stored registrations to see if
        the user's GitHub account is registered with the bot"""

        with open("data/github_registrations.json", "r") as registration_file:
            registrations = json.load(registration_file)
            await ctx.send(
                "You are currently registered on GitHub as "
                f"**{registrations[str(ctx.author.id)]}**.\n"
                "If this is not or is no longer your GitHub username, "
                "!unregister and !register again."
            )

    @commands.command()
    async def unregister(self, ctx):
        """Removes the user's GitHub login from the stored
        registrations if they are already registered"""

        with open("data/github_registrations.json", "w+") as registration_file:
            try:
                del registrations[str(ctx.author.id)]
                await ctx.send(
                    "Your GitHub login has been removed from our server. "
                    "Complete the process by navigating to the following page:\n\n"
                    "<https://github.com/settings/connections/applications/45e2376f056230c072a5>\n\n"
                    "and clicking 'Revoke access'"
                )
            except KeyError:
                await ctx.send(
                    "You have not registered your GitHub account with RUCS24."
                )
            json.dump(registrations, registration_file)


def setup(bot):
    bot.add_cog(GithubCog(bot))
