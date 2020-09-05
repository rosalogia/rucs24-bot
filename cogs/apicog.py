from discord.ext import commands, tasks
import discord
import requests
import json
from fuzzywuzzy import fuzz
import sys

sys.path.append("utilities")
from getsubjects import subject_list
from getclasses import classes_dict
from indextoclass import index_to_class


def check_open(index):
    """Returns true if an entered course is open, false if not"""
    # Request URL to retrieve indexes of all open sections currently
    open_sections_url = (
        "https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=NB"
    )

    # Try catch in case the api call fails
    try:
        # I load the text from requests call into a list called open_sections
        # open_sections now contains indexes of all open sections
        open_sections = json.loads(requests.get(open_sections_url).text)
    except Exception as e:
        print(e)
        return

    # Check if index entered is in open sections
    return index in open_sections


def remove_snipe(user_id, index):
    """Removes the specified snipe from the json"""

    # Load in the current snipes
    with open("apidata/snipes.json", "r") as f:
        snipes_dict = json.load(f)

    # If the snipe exists, remove it, update json, and return true
    # Else, return false
    if user_id in snipes_dict.keys():
        if index in snipes_dict[user_id]:
            snipes_dict[user_id].remove(index)
            with open("apidata/snipes.json", "w") as f:
                json.dump(snipes_dict, f)
            return True
        else:
            return False
    else:
        return False


class ApiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Start the sniper
        self.sniper.start()

    # Loops every 15 seconds
    @tasks.loop(seconds=15)
    async def sniper(self):
        # Not adding a docstring because then it'll be visible in help, only an internal command

        # Get open sections
        open_sections_url = "https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=NB"

        # Try catch in case the api call fails
        try:
            # I load the text from requests call into a list called open_sections
            # open_sections now contains indexes of all open sections
            open_sections = json.loads(requests.get(open_sections_url).text)
        except Exception as e:
            print(e)
            return

        # Load in the snipes
        with open("apidata/snipes.json", "r") as f:
            snipes_dict = json.load(f)

        # Go through every user and snipe
        for user_id in snipes_dict.keys():
            for index in snipes_dict[user_id]:
                if index in open_sections:
                    # Retrieve user object
                    user = self.bot.get_user(int(user_id))

                    # Create dm channel if necessary
                    if user.dm_channel is None:
                        await user.create_dm()

                    # Remove their snipe and alert them
                    remove_snipe(user_id, index)
                    await user.dm_channel.send(
                        f"Section {index} is open! Use !open {index} to see course description! Snipe removed"
                    )

    # Make sure sniper only runs after bot is ready
    @sniper.before_loop
    async def before_printer(self):
        print("Logging on...")
        await self.bot.wait_until_ready()

    @commands.command()
    async def open(self, ctx, index):
        """Takes in course section index and outputs whether the section is open or closed"""

        section = index_to_class[index]

        status = "open" if check_open(index) else "closed"

        embed = discord.Embed(
            title=section["name"], description=section["course"], color=0xFF0000
        )
        embed.add_field(
            name=f'Section {section["section"]}: {section["instructors"]}', value=status
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def lookup(self, ctx, *args):
        """Takes in subject name and allows you to look up courses and sections in that subject"""

        # Store their lookup string, store list of subject strings
        lookup_string = " ".join(args)
        subject_options = [x["description"] for x in subject_list]
        subject_match = (0, "")

        # Go through all subject options and find the best fuzzy search match to lookup string
        for subject in subject_options:
            ratio = fuzz.token_set_ratio(lookup_string, subject)
            if ratio > subject_match[0]:
                subject_match = (ratio, subject)

        # Initialize mapping from course titles to objects, subject titles to objects, and list for course titles
        courses = {x["title"]: x for x in classes_dict[subject_match[1]]}
        subjects = {x["description"]: x for x in subject_list}
        course_titles = [k for (k, v) in courses.items()]

        # Separate course titles by commas
        course_str = ", ".join(course_titles)

        # Display all the course options from the best match
        embed = discord.Embed(
            title=f"Showing results for {subject_match[1]}",
            description="Please choose a course",
            color=0xFF0000,
        )
        embed.add_field(
            name="Type in a course name to see available sections", value=course_str
        )
        await ctx.send(embed=embed)

        def check(m):
            """Quick check to make sure only the person in the game and channel can respond"""
            return m.channel == ctx.channel and m.author == ctx.author

        # Wait for their course choice
        msg = await self.bot.wait_for("message", check=check)

        # Keep prompting until it's a valid course
        while msg.content.upper() not in course_titles:
            await ctx.send("Please enter course name exactly, case doesn't matter")
            msg = await self.bot.wait_for("message", check=check)

        # Get their course object from the map
        chosen_course = courses[msg.content.upper()]

        # Set up an embed title and description with their course
        embed = discord.Embed(
            title=f"{subject_match[1]}, {msg.content.upper()}",
            description=f'01:{subjects[subject_match[1]]["code"]}:{chosen_course["courseNumber"]}',
            color=0xFF0000,
        )

        # Go through all the sections of the course
        for section in chosen_course["sections"]:
            # Set up variables describing the section
            index = section["index"]
            status = "open" if check_open(index) else "closed"
            number = section["number"]
            profs = "; ".join([x["name"] for x in section["instructors"]])

            # Add a field for that section
            embed.add_field(
                name=f"{number}, {index}\n{profs}", value=f"Status: {status}"
            )

        # Send the section data
        await ctx.send(embed=embed)

    @commands.command()
    async def addsnipe(self, ctx, index):
        """Adds a snipe of the specified index to the user"""

        # Get snipes dict
        with open("apidata/snipes.json", "r") as f:
            snipes_dict = json.load(f)

        author_id = str(ctx.author.id)

        # If they're not stored already, create an empty list for them
        if not author_id in snipes_dict.keys():
            snipes_dict[author_id] = []

        # If they already have the snipe, tell them
        if index in snipes_dict[author_id]:
            await ctx.send("You already have this snipe!")
            return
        else:
            snipes_dict[author_id].append(index)

        # Dump the new dict and alert user
        with open("apidata/snipes.json", "w") as f:
            json.dump(snipes_dict, f)

        await ctx.send("Snipe successfully added!")

    @commands.command()
    async def removesnipe(self, ctx, index):
        """Removes a snipe of the specified index from the user"""

        # Simply used remove_snipe and outputted to the user
        if remove_snipe(str(ctx.author.id), index):
            await ctx.send("Snipe removed!")
        else:
            await ctx.send("Did you even have that snipe?")

    @commands.command()
    async def snipes(self, ctx):
        """List all of your snipes"""

        # Load in snipes
        with open("apidata/snipes.json", "r") as f:
            snipes_dict = json.load(f)

        # If they have no snipes, output that, otherwise output all their snipes
        if (
            str(ctx.author.id) not in snipes_dict.keys()
            or len(snipes_dict[str(ctx.author.id)]) == 0
        ):
            await ctx.send("You don't have any snipes yet!")
        else:
            await ctx.send(", ".join([x for x in snipes_dict[str(ctx.author.id)]]))


def setup(bot):
    bot.add_cog(ApiCog(bot))
