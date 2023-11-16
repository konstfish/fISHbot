'''
     _____
   \-     -/
\_/         \
|        0 0 |          fISHbot v1.1.6
|_   <  ) 3  )
/ \         /
   /-_____-\

'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

import time
import yaml
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
import sys
import random
import requests
import json, inspect
import functools
import re

from functions.functions import *
from functions.mail import *

from functions.progress.bar import ShadyBar

from storage.variables import *

#version = "fISHbot1.1.6"

print("     _____")
print("   \\-     -/")
print("\\_/         \\")
print("|        0 0 |")
print("|_   <  ) 3  )")
print("/ \\         /")
print("   /-_____-\\")

print(str(version) + " starting up")

startup_extentions = ["cogs.music", "cogs.owstats", "cogs.osu", "cogs.fishfacts", "cogs.memes", "cogs.translate", "cogs.general", "cogs.wikis", "cogs.fishing", "cogs.admin"]

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='f!', intents=intents)

@bot.event
async def on_ready():
    print("Logged in as: " + str(bot.user.name))
    print("ID: " + str(bot.user.id))
    print(str(version) + " loaded")
    #await bot.change_presence(game=discord.Game(name='on konst.fish/bot | f!help', url="https://konst.fish", type=1))
    print("Bot live in these Servers:")
    for server in bot.guilds:
        print(server, end=', ')
    print("")

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=("This command is on a %.2fs cooldown!" % error.retry_after), url="", description="", color=0x3D3D5D)
        await bot.send_message(ctx.message.channel, embed=em)

    elif isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title="Command not recognised!", url="", description="", color=0x3D3D5D)
        em.set_footer(text="f!help for a list of all commands")
        tmp = await bot.send_message(ctx.message.channel, embed=em)
        await asyncio.sleep(10)
        await bot.delete_message(tmp)

    else:
        rng = str(random.randint(00000000, 99999999))
        em = discord.Embed(title=("@fISH#0002 fucked something up lmao"), description=(str(error)), colour=0x3D3D5D)
        em.set_footer(text=("Error ID: " + str(rng)))
        deletdis = await bot.send_message(ctx.message.channel, embed=em)
        print(str(rng))
        raise error
        await asyncio.sleep(10)
        await bot.delete_message(deletdis)
        print("mailing")
        mailme(str(error), str(rng), ctx)


#@bot.event
#async def on_command(command, ctx):
    # pass

bot.remove_command("help")

'''

    admin com

'''

@bot.command(pass_context=True)
async def reload(ctx):
    if (str(ctx.message.author.id) == "196328425508700160"):
        start = time.clock()
        em=discord.Embed(title="⚙️ Reloading extensions...", color=0x3D3D5D)
        tmp = await bot.say(embed=em)
        errors = ""
        for extention in startup_extentions:
             try:
                 bot.unload_extension(extention)
                 await asyncio.sleep(0.1)
                 bot.load_extension(extention)
             except Exception as e:
                 print(e)
                 exc = "{}: {}".format(type(e).__name__, e)
                 print("Failed to load extension {}".format(extention, exc))
                 errors += ("Failed to load extension {}".format(extention, exc))
                 errors += " - " + str(e) + "\n"
        if(errors == ""):
            errors = "None"
        emz=discord.Embed(title=("🔧 Reload Complete."), description=("Errors:\n" + errors), color=0x3D3D5D)
        acc = ("%.2f" % ((time.clock() - start) * 1000))
        emz.set_footer(text="Task completed in " + str(acc) + "ms")
        await bot.edit_message(tmp, embed=emz)
        await asyncio.sleep(15)
        await bot.delete_message(tmp)
        return
    else:
        em = discord.Embed(title="Command not recognised!", url="", description="", color=0x3D3D5D)
        em.set_footer(text="f!help for a list of all commands")
        tmp = await bot.send_message(ctx.message.channel, embed=em)
        await asyncio.sleep(10)
        await bot.delete_message(tmp)


#end
if __name__ == "__main__":
    bar = ShadyBar('Loading Extensions..', max=len(startup_extentions), suffix='%(percent)d%%')
    err = 0
    for extention in startup_extentions:
        try:
            bot.load_extension(extention)
        except Exception as e:
            err = 1
            #print(e)
            exc = "{}: {}".format(type(e).__name__, e)
            #print("Failed to load extension {}".format(extention, exc)
        #bar.next()
    bar.finish()
    if(err):
        print("Error loading one of the extensions. No fancy bar effects :(")

load_dotenv()

bot.run(os.getenv("BOT_KEY"))
