import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import asyncio

import time
import datetime

from storage.variables import *

def __init__(self, bot):
        self.bot = bot

class admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def log(self, ctx,*,string=None):
        if (str(ctx.message.author.id) == "196328425508700160"):
            em=discord.Embed(title="⚙️ Logging...", color=0x3D3D5D)
            tmp = await self.bot.say(embed=em)
            now = datetime.datetime.now().strftime("%d.%m-%y_%H:%M")
            start = time.clock()
            filename = ("fbot_" + now + ".log")
            errors = ""
            file = open(("logs/" + str(filename)), "w")

            logging_data = str(version) + " Log from the " + str(now) + "\n"

            uptime = ""
            sec = int(time.time() - startTime)
            d = 0
            h = 0
            m = 0

            while(sec - 86400 >= 1):
                sec -= 86400
                d += 1
            while(sec - 3600 >= 1):
                sec -= 3600
                h += 1
            while(sec - 60 >= 1):
                sec -= 60
                m += 1

            if(d != 0):
                uptime += (str(d) + "Days ")
            if(h != 0):
                uptime += (str(h) + "h ")
            uptime += (str(m) + "min ")
            uptime += (str(sec) + "sec ")

            logging_data += ("Uptime: " + uptime + "\n")
            logging_data += "..."

            file.write(logging_data)

            file.close()

            if(errors == ""):
                errors = "None"
            emz=discord.Embed(title=("🔧 Logging Complete. Saved Log as " + filename), description=("Errors discovered while logging: " + errors), color=0x3D3D5D)
            acc = ("%.2f" % ((time.clock() - start) * 1000))
            emz.set_footer(text="Task completed in " + str(acc) + "ms")
            await self.bot.edit_message(tmp, embed=emz)
            await asyncio.sleep(25)
            await self.bot.delete_message(tmp)
            return
        else:
            em = discord.Embed(title="Command not recognised!", url="", description="", color=0x3D3D5D)
            em.set_footer(text="f!help for a list of all commands")
            tmp = await self.bot.send_message(ctx.message.channel, embed=em)
            await asyncio.sleep(20)
            await self.bot.delete_message(tmp)


def setup(bot):
    bot.add_cog(admin(bot))
    #print('admin loaded')


'''
@bot.command(pass_context=True)
async def mkvc(ctx, *args):
    await self.bot.send_typing(ctx.message.channel)
    if(len(args) ==  0):
        em = discord.Embed(title=('Wrong syntax bastard'), description="", colour=0x3D3D5D)
        await self.bot.say(embed=em)
    else:
        try:
            await self.bot.create_channel(ctx.message.server, (args[0]), type=discord.ChannelType.voice)
        except:
            em = discord.Embed(title=('No clue what went wrong to be honest. Illegal characters in the channel name could be an issue.'), description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)

@bot.command(pass_context=True)
async def mktc(ctx, *args):
    await self.bot.send_typing(ctx.message.channel)
    if(len(args) ==  0):
        em = discord.Embed(title=('Wrong syntax bastard'), description="", colour=0x3D3D5D)
        await self.bot.say(embed=em)
    else:
        try:
            await self.bot.create_channel(ctx.message.server, (args[0]), type=discord.ChannelType.text)
        except:
            em = discord.Embed(title=('No clue what went wrong to be honest. Illegal characters in the channel name could be an issue.'), description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
'''
