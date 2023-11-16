import asyncio
import discord
from discord.ext import commands
import random
from functions.functions import *

import wikipedia
import urbandictionary as ud

def __init__(self, bot):
        self.bot = bot

class wikis:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def urbandict(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        try:
            defs = ud.define(tag)
        except:
            em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        em = discord.Embed(title=defs[0].word, description="", colour=0x3D3D5D)
        em.add_field(name="Definition", value=defs[0].definition, inline=False)
        em.add_field(name="Example", value=("```" + defs[0].example + "```"), inline=True)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def wiki(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        try:
            wiki = wikipedia.page(tag)
        except:
            em = discord.Embed(title="Wrong Syntax / Article doesn't exist.", description="", colour=0x3D3D5D)
            await bot.say(embed=em)

        try:
            em = discord.Embed(title="Article Link", description=wiki.summary, url=wiki.url, colour=0x3D3D5D)
            em.set_author(name=wiki.title)
            em.set_thumbnail(url=wiki.images[00])
            await self.bot.say(embed=em)
        except:
            em = discord.Embed(title="Article too long :(", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(wikis(bot))
    #print('wikis loaded')
