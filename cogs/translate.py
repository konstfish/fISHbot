import asyncio
import discord
from discord.ext import commands

from functions.functions import *


def __init__(self, bot):
        self.bot = bot

class gtranslate:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def translate(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        try:
            ausg = "*" + translateg(tag) + "*"
        except:
            em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        em = discord.Embed(title="Translation:", description=ausg, colour=0x3D3D5D)
        em.set_footer(text="You can also use !t")
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def t(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        try:
            ausg = "*" + translateg(tag) + "*"
        except:
            em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        em = discord.Embed(title="Translation:", description=ausg, colour=0x3D3D5D)
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(gtranslate(bot))
    #print('translate loaded')
