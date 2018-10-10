import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

f = open('storage/fishFacts.txt', encoding='utf-8')
facts = f.readlines()
f.close()


def __init__(self, bot):
        self.bot = bot

class fishfacts:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def fishfact(self, ctx,*,string=None):
        i = 1
        if (string == "spam"):
            i = 4
        while i != 0:
            which = random.randint(0, (len(facts) - 1))
            em = discord.Embed(title=facts[which], description="", colour=0x3D3D5D)
            em.set_author(name="FishFact #" + str(which), icon_url='https://i.imgur.com/OCHWSCA.png')
            await self.bot.say(embed=em)
            i -= 1

    @commands.command(pass_context=True)
    async def factamount(self, ctx):
        await self.bot.say("There are " + str(len(facts)) + " fish facts in the fishFacts file.")

def setup(bot):
    bot.add_cog(fishfacts(bot))
    #print('fishfacts loaded')
