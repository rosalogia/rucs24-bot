from discord.ext import commands
import discord
import json


class ReactCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.has_role("Admin") #Only for admins
    async def addreactionrole(self, ctx, channel, num_rr_str, *args):
        """Enter channel name, number of reaction roles, and message to send, sends reaction role msg"""
        def check(m):
            """Quick check to make sure only the person in the channel can respond"""
            return m.channel == ctx.channel and m.author == ctx.author
        
        def check_r(reaction, user):
            """Quick check to make sure only the ctx user can react"""
            return user == ctx.author

        #Collect their message, number of reaction roles, and channel
        text = ' '.join(args)
        num_rr = int(num_rr_str)
        rr_channel = discord.utils.get(ctx.guild.text_channels, name=channel)

        #Exit if their channel is invalid
        if rr_channel == None:
            await ctx.send('Channel not found!')
            return
        
        react_roles = {}

        #Go through all the reaction roles they want to add
        for i in range(1, num_rr+1):
            #Get the role name they want
            await ctx.send(f'Enter the name of role {i}')
            role_name = await self.bot.wait_for('message', check=check)

            #Keep collecting it until it's a valid role
            while discord.utils.get(ctx.author.guild.roles, name=role_name.content) == None:
                await ctx.send(f'Invalid role name! Try again')
                role_name = await self.bot.wait_for('message', check=check)
            
            #Collect the corresponding emoji reaction
            await ctx.send('React with the corresponding emoji')
            reaction, user = await self.bot.wait_for('reaction_add', check=check_r)
            reaction_emoji = str(reaction.emoji)
            
            #Map emoji to role name
            react_roles[reaction_emoji] = role_name.content
        
        #Send their message
        bot_msg = await rr_channel.send(text)

        #Add all their reactions
        for k in react_roles.keys():
            await bot_msg.add_reaction(k)
        
        #Load in the current reaction roles
        with open('apidata/reactroles.json', 'r') as f:
            rr_dict = json.load(f)
            rr_dict[str(bot_msg.id)] = react_roles
        
        #Dump the updated dict
        with open('apidata/reactroles.json', 'w') as f:
            json.dump(rr_dict, f)
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Adds proper reaction roles"""

        #Store message id, emoji, and member
        message_id = payload.message_id
        emoji = str(payload.emoji)
        
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        #Load the rr dict
        with open('apidata/reactroles.json', 'r') as f:
            rr_dict = json.load(f)
        
        #Go through all the reaction roled messages
        for k in rr_dict.keys():
            #If there's a match, try to fetch role name from rr_dict
            if str(message_id) == k:
                try:
                    role_name = rr_dict[k][emoji]
                except:
                    return
                
                #Get the role object and add the role
                role = discord.utils.get(member.guild.roles, name=role_name)
                await member.add_roles(role)
                return
                
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Removes proper reaction roles"""

        #Literally the same but removes the role
        message_id = payload.message_id
        emoji = str(payload.emoji)

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        with open('apidata/reactroles.json', 'r') as f:
            rr_dict = json.load(f)
            
        for k in rr_dict.keys():
            if str(message_id) == k:
                try:
                    role_name = rr_dict[k][emoji]
                except:
                    return
                
                role = discord.utils.get(member.guild.roles, name=role_name)
                await member.remove_roles(role)
                return

def setup(bot):
    bot.add_cog(ReactCog(bot))