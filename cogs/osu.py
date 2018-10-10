import asyncio
import discord
from discord.ext import commands
from osuapi import OsuApi, AHConnector

def __init__(self, bot):
        self.bot = bot

osuapi = OsuApi("84d15a0b2e5c0930de9126cccb13c9cb96909a07", connector=AHConnector())

class oss:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def osu(self, ctx, *, tag=None):
        await self.bot.send_typing(ctx.message.channel)
        if(tag == None):
            em = discord.Embed(title="Enter a Name bitch", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return
        try:
            #results = osuapi.get_user(tag)
            results = await osuapi.get_user(tag)
        except:
            em = discord.Embed(title="Something went wrong :( (User not found)", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        try:
            em = discord.Embed(title="osu!", url=("https://osu.ppy.sh/users/" + str(results[0].user_id)), colour=0xB81979)
            em.set_author(name=tag, icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Osulogo.png/286px-Osulogo.png", url=("https://osu.ppy.sh/users/" + str(results[0].user_id)))

            em.add_field(name="Rank", value=results[0].pp_rank, inline=True)
            em.add_field(name="pp", value=results[0].pp_raw, inline=True)
            em.add_field(name="Playcount", value=results[0].playcount, inline=True)

            acc = ("%.2f" % results[0].accuracy)
            acc = str(acc) + "%"
            em.add_field(name="Accuracy", value=str(acc), inline=True)

            em.add_field(name="Level", value=results[0].level, inline=True)
            em.add_field(name="Country", value=results[0].country, inline=True)

            em.add_field(name="SS", value=results[0].count_rank_ss, inline=True)
            em.add_field(name="S", value=results[0].count_rank_s, inline=True)
            em.add_field(name="A", value=results[0].count_rank_a, inline=True)

            em.add_field(name="ID", value=results[0].user_id, inline=True)
        except:
            em = discord.Embed(title="Something went wrong :( (Request Failed)", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def osutop(self, ctx, *data):
        await self.bot.send_typing(ctx.message.channel)
        try:
            if(data[0] == None):
                em = discord.Embed(title="Enter a Name bitch", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return
        except:
            em = discord.Embed(title="Enter a Name bitch", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        em = discord.Embed(title="Number of plays?", description="", colour=0x3D3D5D)
        bait = await self.bot.say(embed=em)
        await self.bot.add_reaction(bait, '1⃣')
        await self.bot.add_reaction(bait, '2⃣')
        await self.bot.add_reaction(bait, '3⃣')
        res = await self.bot.wait_for_reaction(('1⃣', '2⃣', '3⃣'), user=ctx.message.author, message=bait)
        await self.bot.delete_message(bait)

        if (res.reaction.emoji == '1⃣'):
            num = 1
        elif (res.reaction.emoji == '2⃣'):
            num = 2
        else:
            num = 3

        try:
            plays = await osuapi.get_user_best(str(data[0]), limit=num)
        except:
           em = discord.Embed(title="Something went wrong :( (User not found)", description="", colour=0x3D3D5D)
           await self.bot.say(embed=em)
           return

        i = 1
        for play in plays:
            bm = await osuapi.get_beatmaps(beatmap_id=play.beatmap_id)
            try:
                await self.bot.send_typing(ctx.message.channel)

                beatmap_data = (" - " + str(bm[0].title) + " [" + str(bm[0].version) + "] by " + str(bm[0].creator))

                em = discord.Embed(title=("#" + str(i) + beatmap_data), description="", url=("https://osu.ppy.sh/b/" + str(play.beatmap_id)), colour=0xB81979)

                em.add_field(name="pp", value=play.pp, inline=True)

                #getting acc
                acc = (int(play.count300) * 300 + int(play.count100) * 100 + int(play.count50) * 50 + int(play.countmiss) * 0)
                acc = acc / ((int(play.count300) + int(play.count100) + int(play.count50) + int(play.countmiss)) * 300)#
                acc = acc * 100
                accu = ("%.2f" % acc)
                accu = str(accu) + "%"

                em.add_field(name="Accuracy", value=accu, inline=True)
                em.add_field(name="Max Combo", value=(str(play.maxcombo) + "x"), inline=True)

                em.add_field(name="Misses", value=(str(play.countmiss) + "x"), inline=True)
                em.add_field(name="Score", value=play.score, inline=True)
                em.add_field(name="Mods", value=play.enabled_mods, inline=True)

                em.set_footer(text=("300: " + str(play.count300) + "x  |  100: " + str(play.count100) +  "x  |  50: " + str(play.count50) + "x"))
                em.set_thumbnail(url=("https://osu.ppy.sh/images/badges/score-ranks/Score-"+ str(play.rank) +"-Small-60.png"))

                await self.bot.say(embed=em)
                i += 1
            except:
                em = discord.Embed(title="Something went wrong :(", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def osur(self, ctx, *data):
        await self.bot.send_typing(ctx.message.channel)
        try:
            if(data[0] == None):
                em = discord.Embed(title="Enter a Name bitch", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return
        except:
            em = discord.Embed(title="Enter a Name bitch", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        em = discord.Embed(title="Number of plays?", description="", colour=0x3D3D5D)
        bait = await self.bot.say(embed=em)
        await self.bot.add_reaction(bait, '1⃣')
        await self.bot.add_reaction(bait, '2⃣')
        await self.bot.add_reaction(bait, '3⃣')
        res = await self.bot.wait_for_reaction(('1⃣', '2⃣', '3⃣'), user=ctx.message.author, message=bait)
        await self.bot.delete_message(bait)

        if (res.reaction.emoji == '1⃣'):
            num = 1
        elif (res.reaction.emoji == '2⃣'):
            num = 2
        else:
            num = 3

        try:
            plays = await osuapi.get_user_recent(str(data[0]), limit=num)
        except:
           em = discord.Embed(title="Something went wrong :( (User not found)", description="", colour=0x3D3D5D)
           await self.bot.say(embed=em)
           return

        i = 1
        for play in plays:
            bm = await osuapi.get_beatmaps(beatmap_id=play.beatmap_id)
            try:
                await self.bot.send_typing(ctx.message.channel)

                beatmap_data = (" - " + str(bm[0].title) + " [" + str(bm[0].version) + "] by " + str(bm[0].creator))

                em = discord.Embed(title=("#" + str(i) + beatmap_data), description="", url=("https://osu.ppy.sh/b/" + str(play.beatmap_id)), colour=0xB81979)

                try:
                    em.add_field(name="pp", value=play.pp, inline=True)
                except:
                    pass
                #getting acc
                acc = (int(play.count300) * 300 + int(play.count100) * 100 + int(play.count50) * 50 + int(play.countmiss) * 0)
                acc = acc / ((int(play.count300) + int(play.count100) + int(play.count50) + int(play.countmiss)) * 300)#
                acc = acc * 100
                accu = ("%.2f" % acc)
                accu = str(accu) + "%"

                em.add_field(name="Accuracy", value=accu, inline=True)
                em.add_field(name="Max Combo", value=(str(play.maxcombo) + "x"), inline=True)

                em.add_field(name="Misses", value=(str(play.countmiss) + "x"), inline=True)
                em.add_field(name="Score", value=play.score, inline=True)
                em.add_field(name="Mods", value=play.enabled_mods, inline=True)

                em.set_footer(text=("300: " + str(play.count300) + "x  |  100: " + str(play.count100) +  "x  |  50: " + str(play.count50) + "x"))
                em.set_thumbnail(url=("https://osu.ppy.sh/images/badges/score-ranks/Score-"+ str(play.rank) +"-Small-60.png"))

                await self.bot.say(embed=em)
                i += 1
            except:
                em = discord.Embed(title="Something went wrong :(", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(oss(bot))
    #print('osu! loaded')
