import discord
from datetime import datetime as time
from discord.ext import commands
import pymongo
import os
import random

class Info(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.colors = [0x7700fe, 0x340e72, 0xfdb706]
        self.TEAM = [838836138537648149,
                               728260210464129075,
                               664550550527803405,
                               693375549686415381,
                               555452986885668886] # our team's discord ids

    #### User Information ####
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member= None):
        if not member:
            member = ctx.author
        if member.id == self.bot.user.id:
            await ctx.invoke(self.bot.get_command('yourinfo'))
        else:
            ## Connect with database ##
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            #tb = db["challenge_data"]
            tb = db['all_about_challenge']
            
            find_user = tb.find_one({"user_id": member.id, "guild_id": member.guild.id})
            roles = []
            for role in member.roles:
                if role.name != '@everyone':
                    role_format = f'{role}'
                    roles.append(role_format)
                    
            #### Information Variables ####
            roles_format = '\n'.join(f'{i}. {j}' for i, j in enumerate(roles, 1)) if len(roles) != 0 else 'No Roles'
            guild = member.guild
            user_id = member.id
            user_name = member.name
            user_tag = member.discriminator
            user_nickname = member.nick
            user_status = str(member.status)
            user_avatar = str(member.avatar_url)
            status_emoji = {
                'online': '<:online:848818909292658729>:', 
                'offline': '<:offline:848818930830016533>', 
                'invisible': '<:offline:848818930830016533>',
                'idle': '<:idle:848818891446681620>',
                'dnd': '<:dnd:848819104446283806>', 
                'do_not_disturb': '<:dnd:848819104446283806>',
            }
            badges_value = {
                0: None,
                1 << 0: 'Discord Employee',
                1 << 1: 'Partnered Server Owner',
                1 << 2: 'HypeSquad Events',
                1 << 3: 'Bug Hunter Level 1',
                1 << 6: 'House Bravery',
                1 << 7: 'House Brilliance',
                1 << 8: 'House Balance',
                1 << 9: 'Early Supporter',
                1 << 10: 'Team User',
                1 << 14: 'Bug Hunter Level 2',
                1 << 16: 'Verified Bot',
                1 << 17: 'Early Verified Bot Developer',
                1 << 18: 'Discord Certified Moderator'
            }
            
            user_activities = member.activities
            status = user_status.captitalize() if user_status != 'dnd' else user_status.upper()
            
            user_badges = ''
            user_all_badges = member.public_flags.all()
            for no, badge in enumerate(user_all_badges, 1):
                value = badge.value
                user_badge+= f'{no}. {badges_value[value]}\n'
            joined_guild = (member.joined_at).strftime('%a, %d-%b-%Y %I:%M %p')
            created_acc = (member.created_at).strftime('%a, %d-%b-%Y %I:%M %p')
            
            #### Embed Part ####
            info_em = discord.Embed(title= 'User Information', color= random.choice(self.colors))
            info_em.add_field(name= 'Name', value= f'```\n{user_name}\n```', inline= True)
            info_em.add_field(name= 'Tag', value= f'```\n#{user_tag}\n```', inline= True)
            info_em.add_field(name= 'ID', value= f'```\n{user_id}\n```', inline= False)
            if user_nickname:
                info_em.add_field(name= 'Nickname', value= f'```\n{user_nickname}\n```', inline= False)
            info_em.add_field(name= 'Status', value= f'{status_emoji[user_status]} - {status}', inline= False)
            info_em.add_field(name= f'Joined {guild.name} at', value= f'```\n{joined_guild} UTC\n```', inline= False)
            info_em.add_field(name= 'Account Created at', value= f'```\n{created_acc} UTC\n```', inline= False)
            info_em.add_field(name= 'Badges', value= user_badges, inline= False) if not user_badge else None
            #### challenge's information ####
            if find_user:
                output = f"Level: {find_user['level']}\nXP: {find_user['xp']}/{find_user['need_xp']}"
                info_em.add_field(name= "Challenge Profile", value= output, inline= False)
                challenges_name = find_user["challenges"]
                if challenges_name:
                    all_challenges = ""
                    for no, challenge_name in enumerate(challenges_name, 1):
                        all_challenges += f"{no}. {challenge_name}\n"
                    info_em.add_field(name= "Solved Challenges", value= f"```\n{all_challenges}\n```", inline= False)
            ########
            info_em.add_field(name= f'Roles [{len(roles)}]', value= f'```\n{roles_format}\n```', inline= False)
            info_em.set_thumbnail(url= f'{user_avatar}')
            #info_em.set_author(name= f"{self.bot.user.name}", icon_url= f"{self.bot.user.avatar_url}")
            info_em.set_footer(text= f"Requested by {ctx.author} | Programming Hero ")
            
            await ctx.send(embed= info_em)
    
    #### User Avatar ####
    @commands.command(aliases= ['avatar'])
    async def av(self, ctx, member: discord.Member= None):
        if not member:
            member= ctx.author
        av_url = str(member.avatar_url)
        avatar_em = discord.Embed(title= 'Avatar', description= f'{member.mention}', color= random.choice(self.colors))
        avatar_em.set_image(url= f'{av_url}')
        await ctx.send(embed= avatar_em)
    
    #### Server information ####
    @commands.command(aliases= ['guildinfo'])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        guild_emojis = []
        guild_roles = []
        for role in guild.roles:
            if role.name != '@everyone':
                role_format = f'{role}'
                guild_roles.append(role_format)
        
        ### Information Variable ###
        guild_roles = '\n'.join(f'{i}. {j}' for i, j in enumerate(guild_roles, 1))
        guild_name = guild.name
        guild_id = guild.id
        guild_owner = guild.owner
        guild_owner_id = guild.owner_id
        guild_region = str(guild.region).capitalize()
        guild_description = guild.description
        guild_icon = str(guild.icon_url)
        ### Member count ###
        members = guild.member_count
        humans = 0
        online = 0
        offline = 0
        idle = 0
        dnd = 0
        for m in guild.members:
            status = str(m.status)
            if not m.bot:
                humans+=1
            if status == 'online':
                online+=1
            elif status == 'offline' or status == 'invisible':
                offline+=1
            elif status == 'idle':
                idle+=1
            elif status == 'dnd' or status == 'do_not_disturb':
                dnd+=1
        bots = members - humans
        ######
        guild_text_channels = len(guild.text_channels)
        guild_voice_channels = len(guild.voice_channels)
        guild_channels = guild_text_channels + guild_voice_channels
        guild_categories = len(guild.categories)
        
        ### Embed Part ###
        info_em = discord.Embed(title= 'Server Information', color= random.choice(self.colors))
        info_em.add_field(name= 'Name', value= f'{guild_name}', inline= False)
        info_em.add_field(name= 'Guild ID', value= f'```\n{guild_id}\n```', inline= False)
        info_em.add_field(name= 'Owner', value= f'{guild_owner}', inline= False)
        info_em.add_field(name= 'Owner ID', value= f'```\n{guild_owner_id}\n```', inline= False)
        info_em.add_field(name= 'Region', value= f'{guild_region}', inline= False)
        if guild_description:
            info_em.add_field(name= 'Guild Description', value= f'{guild_description}', inline= False)
        info_em.add_field(name= f'Members [{members}]', value= f'```\nHumans: {humans}\nBots: {bots}\n--------------------\nOnline: {online}\nOffline: {offline}\nIdle: {idle}\nDND: {dnd}\n```', inline= False)
        info_em.add_field(name= 'Channels and Categories', value= f'```\nCategories: {guild_categories}\nChannels: {guild_channels}\n--------------------\nText Channels: {guild_text_channels}\nVoice Channels: {guild_voice_channels}\n```', inline= False)
        info_em.add_field(name= 'Roles', value= f'```\n{guild_roles}\n```', inline= False)
        
        info_em.set_thumbnail(url= f'{guild_icon}')
        info_em.set_footer(text= f"Requested by {ctx.author} | Programming Hero ")
        await ctx.send(embed= info_em)
    
    #### User Challenge Profile ####
    @commands.command()
    async def challengeProfile(self, ctx, member: discord.Member= None):
        ## Connect with database ##
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]
        #tb = db["challenge_data"]
        tb = db['all_about_challenge']
        
        if not member:
            member = ctx.author
        find_user = tb.find_one({"user_id": member.id, "guild_id": member.guild.id})
        level = find_user['level']
        xp = find_user['xp']
        need_xp = find_user['need_xp']
        all_challenges = find_user['challenges']
        if all_challenges:
            challenges = ''
            length = len(all_challenges)
            for no, challenge in enumerate(all_challenges, 1):
                if no != length:
                    challenges += f'{no}. {challenge}\n'
                else:
                    challenges += f'⟩ {no}. {challenge}\n'
                
        else:
                challenges = None
                
        info_em = discord.Embed(title= f'{member.name}\'s Challenge Profile', description= f'```\nLevel: {level}\nXP: {xp}/{need_xp}\n```', color= random.choice(self.colors))
        if challenges:
            info_em.add_field(name= 'Solved Challenges', value= f'```\n{challenges}\n```', inline= False)
        else:
            info_em.add_field(name= 'Solved Challenges', value= f'```\nDidn\'t solved any challenges\n```')
        info_em.set_footer(text= f"{ctx.author} | {ctx.guild.name} ")
        await ctx.send(embed= info_em)

    #### Fibu's Information ####
    @commands.command()
    async def yourinfo(self, ctx):
        prefix = '!fibu '
        version = 'v2.0.0'
        RELEASED_ON = 'Jan 1 , 2021'
        TEAM = ''
        for no, id in enumerate(self.TEAM, 1):
            member = await self.bot.fetch_user(id)
            name = member.name
            TEAM += f'{no}. {name}\n'
        
        info_em = discord.Embed(title= 'My Information', description= f'Hey there {ctx.author.mention}!\nI am **Fibu**.\nYour friend and a friendly discord bot.\nI am from [Programming Hero](https://www.programming-hero.com/)', color= 0xfddd0b)
        info_em.add_field(name= 'ID', value= f'```\n{self.bot.user.id}\n```')
        info_em.add_field(name= 'Prefix', value= f'```\n{prefix}\n```\nIt\'s my default prefix.\nFor more prefixes type ```\n!fibu prefixes\n```', inline= False)
        info_em.add_field(name= 'Version', value= f'```\n{version}\n```', inline= False)
        info_em.add_field(name= 'Released on', value= f'```\n{RELEASED_ON}\n```', inline= False)
        info_em.add_field(name="Website | Programming Hero", value="[Programming Hero](https://www.programming-hero.com/)", inline= False)
        info_em.add_field(name="Application | Programming Hero", value="[Android App](https://is.gd/z11RUg)\n[Iphone Version](https://is.gd/eVH92i)", inline= False)
        info_em.add_field(name="Social Media | Programming Hero", value="[Facebook](https://m.facebook.com/programmingHero/)\n[Instagram](https://is.gd/6m3hgd)\n[Twitter](https://twitter.com/ProgrammingHero?s=09)\n[Youtube](https://is.gd/EulQLJ)\n[Pinterest](https://www.pinterest.com/programminghero1/)", inline= False)
        info_em.add_field(name= 'My Team', value= f'```\n{TEAM}\n```\nFor more info about my team type\n```\n!fibu yourteam\n```')
        info_em.set_thumbnail(url= f'{self.bot.user.avatar_url}')
        info_em.set_footer(text= f"Requested by {ctx.author} | Programming Hero")
        
        await ctx.send(embed= info_em)
        
    #### Our Team ####
    @commands.command()
    async def yourteam(self, ctx):
        team_members = []
        for id in self.TEAM:
            user = await self.bot.fetch_user(id)
            team_members.append(str(user))
        
        
        

def setup(bot):
    bot.add_cog(Info(bot))