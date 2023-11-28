import asyncio
import discord
from discord.ext import commands
import overwatch.stats

def __init__(self, bot):
        self.bot = bot

class owboard:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def boardhere(self, ctx,*,tag = None):
        f = open('owboard/test.txt', encoding='utf-8')
        players = f.readlines()
        f.close()
        i = 0
        while i < len(players):
            players[i] = players[i].replace("\n", "")
            i += 1
        emTmp = discord.Embed(title="Constructing Leaderboard", description="", colour=0x3D3D5D)
        tmp = await self.bot.say(embed=emTmp)
        listSr = []
        listUnranked = []
        for player in players:
            try:
                stats = overwatch.stats.query('pc', player)
                listSr.append(int(stats['competitive_rank']))
                print(player)
                print(str(stats['competitive_rank']))
            except:
                players.remove(player)
                listUnranked.append(player)

        print("After Fetch")
        print(players)
        print(listSr)
        print(listUnranked)

        for passnum in range(len(listSr) - 1, 0, -1):
            for i in range(passnum):
                if listSr[i] > listSr[i + 1]:
                    temp = listSr[i]
                    listSr[i] = listSr[i + 1]
                    listSr[i + 1] = temp

                    temp = players[i]
                    players[i] = players[i + 1]
                    players[i + 1] = temp

        print("After Sort")
        print(players)
        print(listSr)
        print(listUnranked)

def setup(bot):
    bot.add_cog(owboard(bot))
    #print('owstats loaded')