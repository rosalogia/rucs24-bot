from discord.ext import commands
import discord
import requests
import json
from fuzzywuzzy import fuzz
import sys
sys.path.append('utilities')
from getsubjects import subject_list
from getclasses import classes_dict
from indextoclass import index_to_class


def check_open(index):
    """Returns true if an entered course is open, false if not"""
    #Request URL to retrieve indexes of all open sections currently
    open_sections_url = "https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=NB"

    #Try catch in case the api call fails
    try:
        #I load the text from requests call into a list called open_sections
        #open_sections now contains indexes of all open sections
        open_sections = json.loads(requests.get(open_sections_url).text)
    except Exception as e:
        print(e)
        return
    
    #Check if index entered is in open sections
    return index in open_sections


class ApiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def open(self, ctx, index):
        """Takes in course section index and outputs whether the section is open or closed"""
        
        section = index_to_class[index]
        
        status = 'open' if check_open(index) else 'closed'

        embed=discord.Embed(title=section["name"], description=section["course"], color=0xff0000)
        embed.add_field(name=f'Section {section["section"]}: {section["instructors"]}', value=status)

        await ctx.send(embed=embed)
    

    @commands.command()
    async def lookup(self, ctx, *args):
        lookup_string = ' '.join(args)
        subject_options = [x['description'] for x in subject_list]
        subject_match = (0, '')

        for subject in subject_options:
            ratio = fuzz.token_set_ratio(lookup_string, subject)
            if ratio > subject_match[0]:
                subject_match = (ratio, subject)

        courses = {x['title']:x for x in classes_dict[subject_match[1]]}
        subjects = {x['description']:x for x in subject_list}
        course_titles = [k for (k, v) in courses.items()]

        course_str = ', '.join(course_titles)

        embed=discord.Embed(title=f"Showing results for {subject_match[1]}", description="Please choose a course", color=0xff0000)
        embed.add_field(name="Type in a course name to see available sections", value=course_str)

        await ctx.send(embed=embed)

        def check(m):
            """Quick check to make sure only the person in the game and channel can respond"""
            return m.channel == ctx.channel and m.author == ctx.author

        msg = await self.bot.wait_for('message', check=check)

        while msg.content.upper() not in course_titles:
            await ctx.send("Please enter course name exactly, case doesn't matter")
            msg = await self.bot.wait_for('message', check=check)
        
        chosen_course = courses[msg.content.upper()]

        embed=discord.Embed(title=f'{subject_match[1]}, {msg.content.upper()}', description=f'01:{subjects[subject_match[1]]["code"]}:{chosen_course["courseNumber"]}', color=0xff0000)
        
        for section in chosen_course['sections']:
            index = section['index']
            status = 'open' if check_open(index) else 'closed'
            number = section['number']
            profs = '; '.join([x['name'] for x in section['instructors']])

            embed.add_field(name=f'{number}, {index}\n{profs}', value=f'Status: {status}')
        
        await ctx.send(embed=embed)







def setup(bot):
    bot.add_cog(ApiCog(bot))