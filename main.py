import discord
from discord.ext import commands
from discord.utils import get

import time
from datetime import datetime
import os
import asyncio
import pymongo
import logging


#### logging [recommended]####
logging.basicConfig(level=logging.INFO)
########

TEAM = [838836138537648149, 728260210464129075, 664550550527803405, 693375549686415381, 555452986885668886] # our team's discord ids

### prefixes ###
prefix_file = open("prefix.txt","r")
fibu_prefixes = [i.replace("\n"," ") for i in prefix_file.readlines()]

intents = discord.Intents.default()
intents.members = True

### bot
bot = commands.Bot(command_prefix= fibu_prefixes, intents= intents, case_insensitive= True, help_command= None)

### on ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!fibu help | Fibu | Programming Hero"))
    print(f"Logged in as {bot.user}")
    
# ping
@bot.command()
async def ping(ctx):
    msg = discord.Embed(title="Pong 🏓", description=f"{round(bot.latency*1000)} _ms_!",color= 0xffdf08)
    await ctx.send(embed= msg)

## prefixes
@bot.command()
async def prefixes(ctx):
    prefixes_format = '1. !fibu \n2. fibu \n3. !f \n4. f! \n'
    msg = f'**__My Prefixes__**\n```\n{prefixes}\n```\n__Example:__\n```\n!fibu help\n```'
    await ctx.message.add_reaction('\N{White Heavy Check Mark}')
    await ctx.author.send(msg)

### cogs load, unload and reload commands
## cogs load
@bot.command()
async def load(ctx, file = "all"):
    if ctx.author.id in TEAM:
        if file=="all":
            loaded_cogs = []
            already_loaded = []
            for files in os.listdir("./cogs"):
                if files.endswith(".py"):
                    try:
                        bot.load_extension(f"cogs.{files[:-3]}")
                        loaded_cogs.append(files[:-3])
                    except:
                        already_loaded.append(files[:-3])
            
            if loaded_cogs!=[]:
                if already_loaded==[]:
                    await ctx.send("All cogs loaded!!")
                else:
                    loaded_cogs = "\n".join(f"{i} loaded!!" for i in loaded_cogs)
                    already_loaded = "\n".join(i+" already loaded!!" for i in already_loaded)
                await ctx.send(f"**__Loaded Cogs__**\n```\n{loaded_cogs}\n```**__Already Loaded Cogs__**\n```\n{already_loaded}\n```")
            else:
                already_loaded = "\n".join(f"{i} already loaded!!" for i in already_loaded)
                await ctx.send(f"**__Already Loaded Cogs__**\n```\n{already_loaded}\n```")
          
        else:
            if os.path.exists(f"cogs/{file}.py"):
                try:
                    bot.load_extension(f"cogs.{file}")
                    await ctx.send(f"{file} loaded!")
                except Exception as e:
                    #await ctx.send(e)
                    await ctx.send(f"{file} is already loaded!")        
            else:
                await ctx.send(f"{file} not found")
    else:
        await ctx.send("You don't have the permission to do that!!")

## cogs unload
@bot.command()
async def unload(ctx, file = "all"):
    if ctx.author.id in TEAM:
        if file=="all":
            unloaded_cogs = []
            already_unloaded = []
            for files in os.listdir("./cogs"):
                if files.endswith(".py"):
                    try:
                        bot.unload_extension(f"cogs.{files[:-3]}")
                        unloaded_cogs.append(files[:-3])
                    except:
                        already_unloaded.append(files[:-3])
            
            if unloaded_cogs!=[]:
                if already_unloaded==[]:
                    await ctx.send("All cogs unloaded!!")
                else:
                    unloaded_cogs = "\n".join(f"{i} unloaded!!" for i in unloaded_cogs)
                    already_unloaded = "\n".join(i+" already unloaded!!" for i in already_unloaded)
                await ctx.send(f"**__Unloaded Cogs__**\n```\n{unloaded_cogs}\n```\n**__Already Unloaded Cogs__**```\n{already_unloaded}\n```")
            else:
                already_unloaded = "\n".join(f"{i} already unloaded!!" for i in already_unloaded)
                await ctx.send(f"**__Already Unloaded Cogs__**\n```\n{already_unloaded}\n```")
          
        else:
            if os.path.exists(f"cogs/{file}.py"):
                try:
                    bot.unload_extension(f"cogs.{file}")
                    await ctx.send(f"{file} unloaded!")
                except Exception as e:
                    #await ctx.send(e)
                    await ctx.send(f"{file} is already unloaded!")        
            else:
                await ctx.send(f"{file} not found")
    else:
        await ctx.send("You don't have the permission to do that!!")
            
## cogs reload
@bot.command()
async def reload(ctx, file = "all"):
    if ctx.author.id in TEAM:
        if file=="all":
            reloaded_cogs = []
            already_unloaded = []
            for files in os.listdir("./cogs"):
                if files.endswith(".py"):
                    try:
                        bot.reload_extension(f"cogs.{files[:-3]}")
                        reloaded_cogs.append(files[:-3])
                    except:
                        already_unloaded.append(files[:-3])
            
            if reloaded_cogs!=[]:
                if already_unloaded==[]:
                    await ctx.send("All cogs reloaded!!")
                else:
                    reloaded_cogs = "\n".join(f"{i} reloaded!!" for i in reloaded_cogs)
                    already_unloaded = "\n".join(i+" already unloaded!!" for i in already_unloaded)
                await ctx.send(f"**__Reloaded Cogs__**\n```\n{reloaded_cogs}\n```\n**__Already Unloaded Cogs__**\n```\n{already_unloaded}\n```")
            else:
                already_unloaded = "\n".join(f"{i} already unloaded!!" for i in already_unloaded)
                await ctx.send(f"```\n**__Already Unloaded Cogs__**\n```\n{already_unloaded}\n```")
          
        else:
            if os.path.exists(f"cogs/{file}.py"):
                try:
                    bot.reload_extension(f"cogs.{file}")
                    await ctx.send(f"{file} reloaded!")
                except Exception as e:
                    #await ctx.send(e)
                    await ctx.send(f"{file} is already unloaded!")        
            else:
                await ctx.send(f"{file} not found")
    else:
        await ctx.send("You don't have the permission to do that!!")



        
### load all cogs
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


token = os.getenv("TOKEN")
bot.run(token)