import asyncio
import discord
from discord.ext import commands
import overwatch.stats

def __init__(self, bot):
        self.bot = bot

class owstats:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def owstats(self, ctx,*,tag = None):
        await self.bot.send_typing(ctx.message.channel)
        if tag == None:
            em = discord.Embed(title="Wrong Syntax.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        urltag = tag.replace('#', '-')

        em = discord.Embed(title="Overbuff", url=("https://www.overbuff.com/players/pc/" + urltag), color=0xfa9c1e)

        if(True):
            emTmp = discord.Embed(title="Fetching Stats...", description="", colour=0x3D3D5D)
            tmp = await self.bot.say(embed=emTmp)
            await self.bot.send_typing(ctx.message.channel)

                #FETCHING STATS

            try:
                stats = overwatch.stats.query('pc', tag)
            except:
                await self.bot.delete_message(tmp)
                em = discord.Embed(title="BattleTag not found", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return

            try:
                rnkst = str(stats['competitive_rank'])
                em.add_field(name="Rank", value=rnkst, inline=True)
            except:
                em.add_field(name="Rank", value="/", inline=True)

            lvlst = str(stats['level'])
            em.add_field(name="Level", value=lvlst, inline=True)

            try:
                maps = ""
                try:
                    gamesw = str(stats['competitive']['overall']['game_won'])
                    gamesp = str(stats['competitive']['overall']['game_played'])
                    maps += "*Played:* " + gamesp + "\n"
                    maps += "*Won:*     " + gamesw + "\n"
                    try:
                        gamesl = str(stats['competitive']['overall']['game_lost'])
                    except:
                        gamesl = " /"
                    maps += "*Lost:*     " + gamesl + "\n"
                except:
                    maps = "/"
                em.add_field(name="Maps", value=maps, inline=True)


                elmst = str(stats['competitive']['overall']['elimination'])
                elmaxst = str(stats['competitive']['overall']['elimination_most_in_game'])
                elmi = "*Most:* "
                elmi += elmaxst + "\n" + "*Total:* " + elmst + "\n"

                em.add_field(name="Eliminations", value=elmi, inline=True)

                solok = str(stats['competitive']['overall']['solo_kill'])
                solokmost = str(stats['competitive']['overall']['solo_kill_most_in_game'])
                solokm = "*Most:* "
                solokm += solokmost + "\n" + "*Total:* " + solok + "\n"

                em.add_field(name="Solo Kills", value=solokm, inline=True)

                killstr = str(stats['competitive']['overall']['kill_streak_best'])
                killstr = "*Best:* " + killstr
                em.add_field(name="Killstreak", value=killstr, inline=True)

                dthst = str(stats['competitive']['overall']['death'])
                dthst = "*Total:* " + dthst
                em.add_field(name="Deaths", value=dthst, inline=True)


                dmgst = str(stats['competitive']['overall']['hero_damage_done'])
                dmgmaxst = str(stats['competitive']['overall']['hero_damage_done_most_in_game'])
                dmgx = "*Most:* "
                dmgx += dmgmaxst + "\n" + "*Total:* " + dmgst + "\n"

                em.add_field(name="Damage", value=dmgx, inline=True)

                hlst = str(stats['competitive']['overall']['healing_done'])
                hlmaxst = str(stats['competitive']['overall']['healing_done_most_in_game'])
                heal = "*Most:* "
                heal += hlmaxst + "\n" + "*Total:* " + hlst + "\n"

                em.add_field(name="Healing", value=heal, inline=True)

                mdlst = str(stats['competitive']['overall']['medal'])
                mdlbst = str(stats['competitive']['overall']['medal_bronze'])
                mdlsst = str(stats['competitive']['overall']['medal_silver'])
                mdlgst = str(stats['competitive']['overall']['medal_gold'])
                mdlstt = "*Total:* "
                mdlstt += mdlst + "\n" + "*Gold:* " + mdlgst + "\n" + "*Silver:* " + mdlsst + "\n" + "*Bronze:* " + mdlbst

                em.add_field(name="Medals", value=mdlstt, inline=True)

                #crdst = str(stats['competitive']['overall']['card'])
                #crdst = "*Total:* " + crdst
                #em.add_field(name="Cards", value=crdst, inline=True)

            except:
                await self.bot.delete_message(tmp)
                em = discord.Embed(title="Something went wrong while fetching one of your stats try agane", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return

            try:
                await self.bot.delete_message(tmp)
                em.set_author(name=tag, icon_url=stats['icon_url'], url=("https://playoverwatch.com/en-us/career/pc/" + urltag))
                em.set_footer(icon_url="https://res.cloudinary.com/teepublic/image/private/s--Ug0iCq1F--/t_Preview/b_rgb:191919,c_limit,f_jpg,h_630,q_90,w_630/v1488911584/production/designs/1298385_1.jpg", text="Stats taken from playoverwatch.com")
                await self.bot.say(embed=em)
            except:
                await self.bot.delete_message(tmp)
                em = discord.Embed(title="Something went wrong at the last stage just go agane", description="", colour=0x3D3D5D)
                await self.bot.say(embed=em)
                return

def setup(bot):
    bot.add_cog(owstats(bot))
    #print('owstats loaded')
