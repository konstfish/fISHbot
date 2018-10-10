import asyncio
import discord
from discord.ext import commands
import random
from giphypop import translate as gftranslate

def __init__(self, bot):
        self.bot = bot

class memes:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5)
    async def tag(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        try:
            if tag[0] != "<":
                em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return
        except:
            em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)

        i = 4
        while i != 0:
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.say(tag)
            i -= 1

    @commands.command(pass_context=True)
    async def b8ll(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        if (tag == None):
            em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
        else:
            answer = ["Yes.", "No.", "Maybe.", "Time's mom is gay.", "I hope so.", "My reply is no.", "Don't count on it", "Count on it.", "My sources say no.", "It is certain.", "I dont know.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Reply hazy try again.", "Ask again later.", "Cannot predict now.", "Better not tell you now.", "Concentrate and ask again.", "My reply is no.", "Outlook not so good.", "Very doubtful."]
            rng = random.randint(0, len(answer) - 1)
            em = discord.Embed(title="Question", description=tag, colour=0x000000)
            em.set_author(name="8Ball", icon_url='https://vrmainc.com/wp-content/uploads/2016/02/8ball-son.jpg')
            val = answer[rng]
            em.add_field(name="Answer", value=val, inline=False)
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def meirl(self, ctx):
        await self.bot.say('https://imgur.com/ybgTbdV')

    @commands.command(pass_context=True)
    async def ocelot(self, ctx):
        em = discord.Embed(title="", description="😛", colour=0x3D3D5D)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def gif(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        if (tag == None):
            await self.bot.say("Wrong Syntax!")
        else:
            img = gftranslate(tag, api_key='1a3QKqfxl3jvPBMcLkBG7IkO57MemURs')
            await self.bot.say(img.url)

    @commands.command(pass_context=True)
    async def lit(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        fish = ['🐟', '🐠', '🐡']
        rng = random.randint(0, (len(fish) - 1))
        em = discord.Embed(title="", description=(fish[rng] + "\n🔥"), colour=0x3D3D5D)
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(memes(bot))
    #print('memes loaded')
