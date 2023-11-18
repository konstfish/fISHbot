import asyncio
import discord
from discord.ext import commands
import random
import time
import datetime
import os
from functions.functions import *

from storage.variables import *

def __init__(self, bot):
        self.bot = bot

class general:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx,*,string=None):
        if(string == "fishing"):
            em = discord.Embed(title="Fishing Commands (WIP) - Prefix: f!", url="https://konst.fish/bot",
                               description="- fishing - makes a profile / shows your current stats\n- throwrod - starts a fishing session\n- shop - trades common fish for bait (wip)", color=0x42B6E7)
            await self.bot.say(embed=em)
        else:
            em=discord.Embed(title="Commands - Prefix: f!", url="https://konst.fish/bot", color=0x3D3D5D)

            gerneralCom = "- fishfact\n- translate [text]\n- urbandict [word]\n- wiki [article]\n- crypto [currency]\n- poll [question] [options]\n- status [ip/domain]\n- rng [num1] [num2]\n- gif [search]\n"
            em.add_field(name="General Commands", value=gerneralCom, inline=True)

            gaymingCom ="- owstats [BattleTag]\n- osu [username]\n- osutop [username]\n- osur [username]"
            em.add_field(name="Game Commands", value=gaymingCom, inline=True)

            musicCom = "- join\n- play [anything]\n- volume [1-100]\n- skip\n- stop"
            em.add_field(name="Music Commands", value=musicCom, inline=True)

            fishingCom = "- fishing\n- throwrod\n- shop"
            em.add_field(name="Fishing Game Commands", value=fishingCom, inline=True)

            memeCom =     "- tag [user]\n- b8ll"
            em.add_field(name="Meme Commands", value=memeCom, inline=True)

            if(ctx.message.channel.name.lower() == "nsfw"):
                nsfwcom =     "f!r34\n"
                em.add_field(name="NSFW Commands", value=nsfwcom, inline=True)

            em.set_footer(text="Add me: https://konst.fish/bot")

            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def rng(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        if(tag != None):
            nummer1 = ""
            nummer2 = ""
            num1 = 1
            for char in tag:
                while (num1 == 1):
                    if (char == " "):
                        num1 = 0
                        break
                    nummer1 += char
                    break
                else:
                    nummer2 += char
            try:
                ausg = (random.randint(int(nummer1), int(nummer2)))
            except:
                em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return
            em = discord.Embed(title=ausg, description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(title=(str(random.randint(1, 100))), description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def status(self, ctx, *, tag="konst.fish"):
        start = time.clock()
        await self.bot.send_typing(ctx.message.channel)
        if(tag == "discord"):
            tag = "status.discordapp.com"
        response = os.system("ping -c 1 " + tag)
        if(response == 0):
            em = discord.Embed(title=("Host " + tag + " is up.") , description="", colour=0x3D3D5D)
        else:
            em = discord.Embed(title=("Host " + tag + " is down.") , description="", colour=0x3D3D5D)
        acc = ("%.4f" % ((time.clock() - start) * 1000))
        em.set_footer(text=("Time taken: " + str(acc) + "ms"))
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def crypto(self, ctx, *, tag=None):
            await self.bot.send_typing(ctx.message.channel)
            try:
                ausg = coinMarketCap(tag.lower())
            except:
                em = discord.Embed(title="Check if you spelled the cryptos name correctly and try again!", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return

            em = discord.Embed(title=tag, description=ausg, colour=0x3D3D5D)
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def neofetch(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        uptime = ("Uptime: ")
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

        whole =   "```diff\n"
        whole += ("     _____       " + str(ctx.message.author.name) + "@" + version + "\n")
        whole +=  "   \-     -/     ----\n"
        whole += ("\_/         \    WM: Python3.5.2\n")
        whole += ("|        0 0 |   Host: konst.fish\n")
        whole += ("|_   <  ) 3  )   "+ uptime +"\n")
        whole +=  "/ \         /    Cogs Live: " + (str(len(startup_extentions))) + "\n"
        whole +=  "   /-_____-\     ----"
        whole +=  "```"
        #em = discord.Embed(title=tag, description=whole, colour=0x3D3D5D)
        await self.bot.say(whole)

    @commands.command(pass_context=True)
    async def id(self, ctx):
        em = discord.Embed(title=(str(ctx.message.author.id)), description="", colour=0x3D3D5D)
        await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def ana(self, ctx):
        await self.bot.send_typing(ctx.message.channel)
        out = "Hey, I'm " + str(ctx.message.author.name) +", I am a fellow Ana main just like you all, I play at quite a high level, not as " \
              "high as ML7 but at around 1.8. Speaking of ML7 he is my greatest inspiration in life, I want to be JUST " \
              "like him, I watch his streams everyday, he is even my desktop background, and sometimes, I even fantasize" \
              " about him a little bit. But the fact that he isn't in OWL annoys me so hard because he deserves to be " \
              "there, the whole thing is rigged... Just like ML7 I have a good game sense  and very good mechanical skills, " \
              "but one of the main reasons I can't get higher, other than bad team mates, is for some stupid reason hate " \
              "ana :rage: and get really toxic when I play her, and refuse to change because mercy is boring " \
              "Haha just kidding, I am just a lucky piece of shit with a decent mechanical skill, but the biggest reason" \
              " I am here is because I just am lucky that my team mates can carry me even without having a proper main " \
              "healer, or a Zenyatta to nullify the enemy grav, or just be lucky enough to have your enemies have problems, " \
              "like a bad player or people who are fighting a lot. Speaking of which I don't like to fight, so if you " \
              "ask me to change to mercy because I can't aim and can't peel our zen or keep our genji alive, I will" \
              " leave the voice chat because I can't handle the fact that Zen Mercy combo is far superior than " \
              "anything with ana. The only time the games would be fair for both teams would be that both teams " \
              "have an Ana main just like me or that they just play like bronze cucks, and the second option is " \
              "the  one that happens most of the time because at the higher tier, there aren't that many ana players, " \
              "but don't worry, if there is one, he'll be on your team just so you would have an easy loss : ) " \
              "In conclusion, my parents beat me and that gave me a mental disorder where I can't play mercy because" \
              " she is too boring but so is Reinhardt but I don't see too many main tanks switching to something more " \
              "fun because they're not fucking xxx and want to actually win"
        #em = discord.Embed(title=(str(out)), description="", colour=0x3D3D5D)
        tmp = await self.bot.say(out)
        await asyncio.sleep(30)
        await self.bot.delete_message(tmp)


def setup(bot):
    bot.add_cog(general(bot))
    #print('general loaded')
