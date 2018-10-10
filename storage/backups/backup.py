'''
@bot.command(pass_context=True)
async def fishing(ctx, *args):
    await bot.send_typing(ctx.message.channel)

    try:
        try:
            print(len(args))
            if(args[0]):
                if(args[0][0] != "<" and args[0][(len(args[0]) - 1)] != ">"):
                    em = discord.Embed(title="That's not a user, showing your profile instead.", description="", colour=0x3D3D5D)
                    await bot.say(embed=em)
                    uname = str(ctx.message.author.id)
                    raise Exception('Cucklord cant type')
                else:
                    uname = ""
                    i = 3
                    while (i < (len(args[0]) - 1)):
                        uname += args[0][i]
                        i += 1
            em = discord.Embed(title=( uname + "'s Current Stats" ), description="", colour=0x3D3D5D)
        except:
            uname = str(ctx.message.author.id)
            em = discord.Embed(title="Your Current Stats: ", description="", colour=0x3D3D5D)

        try:
            with open ("fishing/" + uname + ".yml") as ymlfile:
                cfg = yaml.load(ymlfile)

            fish = "*Common:* "
            fish += str(cfg['catches']['catch_common'])
            fish += "\n*Rare:* "
            fish += str(cfg['catches']['catch_rare'])
            fish += "\n*Epic:* "
            fish += str(cfg['catches']['catch_epic'])
            fish += "\n*Legendary:* "
            fish += str(cfg['catches']['catch_legendary'])

            em.add_field(name="Catches:", value=fish, inline=True)

            items = "*Bait:* "
            items += str(cfg['items']['bait'])
            items += " - Increases chances of catching higher ranked fish\n*Rod Level:* "
            items += str(cfg['items']['rod_lvl'])
            items += " - Speeds up the fishing"

            em.add_field(name="Items:", value=items, inline=True)

            footer = getBar(int(cfg['user']['lvl_progress']))
            footer += (" " + str(cfg['user']['lvl_progress']) + "% Progress - Level: " + str(cfg['user']['level']))
            em.set_footer(text=footer)

            #em.set_footer(text='Type "f!help fishing" to get a list of all commands')
            await bot.say(embed=em)
        except:
            if(len(args) >= 1):
                em = discord.Embed(title="That user has not created a profile yet.", description="", colour=0x3D3D5D)
                await bot.say(embed=em)
                return
            else:
                try:
                    default = dict(
                        catches=dict(
                            total_catch=0,
                            catch_common=0,
                            catch_rare=0,
                            catch_epic=0,
                            catch_legendary=0,
                        ),
                        items=dict(
                            rod_lvl=1,
                            bait=10,
                        ),
                        user=dict(
                            name=str(ctx.message.author.name),
                            level=1,
                            lvl_progress=0,
                        )
                    )
                    with open(("fishing/" + str(ctx.message.author.id) + ".yml"), "w") as ymlfile:
                        yaml.dump(default, ymlfile, default_flow_style=False)
                except:
                    em = discord.Embed(
                        title="You have some aids letters in your name and I cant save files with those sorry :(",
                        description="", colour=0x3D3D5D)
                    await bot.say(embed=em)
                    return

                em = discord.Embed(title="Created your profile!", description="", colour=0x3D3D5D)
                await bot.say(embed=em)

    #make default yml file
    except:
        em = discord.Embed(title="wtf did you do", description="", colour=0x3D3D5D)
        await bot.say(embed=em)


@bot.command(pass_context=True)
async def throwrod(ctx, *, tag=None):
    await bot.send_typing(ctx.message.channel)
    try:
        with open ("fishing/" + str(ctx.message.author.id) + ".yml") as ymlfile:
            cfg = yaml.load(ymlfile)
    except:
        em = discord.Embed(title='You have to create a profile with "f!fishing" first!', description="", colour=0x3D3D5D)
        await bot.say(embed=em)
        return

    useBait = False
    if(cfg['items']['bait'] != 0):
        em = discord.Embed(title=('Want to use bait?'), description="", colour=0x3D3D5D)
        bait = await bot.say(embed=em)
        await bot.add_reaction(bait, '✅')
        await bot.add_reaction(bait, '❌')
        res = await bot.wait_for_reaction(('✅', '❌'), user=ctx.message.author, message=bait)
        await bot.delete_message(bait)

        if(res.reaction.emoji == '✅'):
            cfg['items']['bait'] -= 1
            useBait = True

    em = discord.Embed(title=(str(ctx.message.author.name) + ' started fishing with a level ' + str(cfg['items']['rod_lvl']) + ' Rod!'), description="", colour=0x3D3D5D)
    tmp = await bot.say(embed=em)

    #await bot.send_typing(ctx.message.channel)

    fishlstfull = ["🐟", "🐡", "🐠", "🦈", "🐳", "🐬", "🦀", "🦐", "🦑"]
    fishlst = []
    rang = 0
    while ((len(fishlst)) != 6):
        rang = random.randint(0, (len(fishlstfull) -1 ))
        if(fishlstfull[rang] not in fishlst):
            fishlst.append(fishlstfull[rang])

    for fishem in fishlst:
        await bot.add_reaction(tmp,fishem)


    react = random.randint(0, (len(fishlst) - 1))
    await asyncio.sleep(random.randint(5, 10))
    em = discord.Embed(title=("React with " + str(fishlst[react]) + " " + str(ctx.message.author.name) + "!"), description="", colour=0x3D3D5D)
    await bot.edit_message(tmp, embed=em)

    res = await bot.wait_for_reaction(str(fishlst[react]), user=ctx.message.author, timeout=1.5, message=tmp)
    if(res != None):
        cfg['catches']['total_catch'] += 1
        rank = ["Common", "Rare", "Epic", "Legendary"]
        j = random.randint(1, 100)
        j = float(j)

        chCom = 70 / float( str("1.00" + str(cfg['items']['rod_lvl'])))
        chRar = 85 / float( str("1.00" + str(cfg['items']['rod_lvl'])))
        chLeg = 98.5 / float( str("1.00" + str(cfg['items']['rod_lvl'])))

        if(useBait):
            chCom -= 1.5
            chRar -= 1.5
            chLeg -= 1.5

        if(j < chCom):
            i = 0
            cfg['catches']['catch_common'] += 1
            cfg['user']['lvl_progress'] += 5
        elif(j < chRar):
            i = 1
            cfg['catches']['catch_rare'] += 1
            cfg['user']['lvl_progress'] += 10
        elif(j < chLeg):
            i = 2
            cfg['catches']['catch_epic'] += 1
            cfg['user']['lvl_progress'] += 15
        else:
            i = 3
            cfg['catches']['catch_legendary'] += 1
            cfg['user']['lvl_progress'] += 25
        if(i == 2):
            em = discord.Embed(title=(str(ctx.message.author.name) +' caught an ' + rank[i] + "  " + fishlst[react] +" !"), description="", colour=0x3D3D5D)
        else:
            em = discord.Embed(title=(str(ctx.message.author.name) + ' caught a ' + rank[i] + "  " + fishlst[react] + " !"),description="", colour=0x3D3D5D)

        if(cfg['user']['lvl_progress'] >= 100):
            cfg['user']['level'] += 1
            cfg['user']['lvl_progress'] = 0
            emlvlup = discord.Embed(title=('Congrats! ' + ctx.message.author.name + " leveled up to Level " + str(
                cfg['user']['level']) + "!"), description="", colour=0x3D3D5D)
            await bot.say(embed=emlvlup)

        footer = getBar(int(cfg['user']['lvl_progress']))
        footer += (" " + str(cfg['user']['lvl_progress']) + "% Progress - Level: " + str(cfg['user']['level']))
        em.set_footer(text=footer)
        await bot.delete_message(tmp)
        await bot.say(embed=em)

        lvlup = [10, 25, 50, 75, 100, 125, 150, 200, 210, 220, 245, 275, 300]

        if (cfg['catches']['total_catch'] in lvlup):
            cfg['items']['rod_lvl'] += 1
            em = discord.Embed(title=('Congrats! ' + ctx.message.author.name + "'s rod leveled up to Level " + str(
                cfg['items']['rod_lvl']) + "!"), description="", colour=0x3D3D5D)
            await bot.say(embed=em)
    else:
        await bot.delete_message(tmp)
        em = discord.Embed(title='Not fast enough. We go AGANE', description="", colour=0x3D3D5D)
        em.set_footer(text="Your stats have been updated.")
        await bot.say(embed=em)

    with open(("fishing/" + str(ctx.message.author.id) + ".yml"), 'w') as ymlfile:
        yaml.dump(cfg, ymlfile, default_flow_style=False)




@bot.command(pass_context=True)
async def shop(ctx, *args):
    await bot.send_typing(ctx.message.channel)
    try:
        with open("fishing/" + str(ctx.message.author.id) + ".yml") as ymlfile:
            cfg = yaml.load(ymlfile)
    except:
        em = discord.Embed(title='You have to create a profile with "f!fishing" first!', description="",
                           colour=0x3D3D5D)
        await bot.say(embed=em)
        return

    reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '❌']

    em = discord.Embed(title=("**Fishing Shop**"), description=("1⃣ - Trade 2 Common fish for 1 Bait\n"
                              "2⃣ - Trade 1 Rare fish for 2 Bait\n"
                              "3⃣ - Trade 1 Epic fish for 4 Bait\n"
                              "4⃣ - Trade 1 Legendary fish for 25 Bait"), colour=0x3D3D5D)
    bait = await bot.say(embed=em)
    for emoji in reactions:
        await bot.add_reaction(bait, emoji)

    res = await bot.wait_for_reaction(('1⃣', '2⃣', '3⃣', '4⃣', '❌'), user=ctx.message.author, message=bait)
    await bot.delete_message(bait)

    if (res.reaction.emoji == '❌'):
        em = discord.Embed(title=("Transaction canceled"), description="", colour=0x3D3D5D)
        bait = await bot.say(embed=em)

    elif (res.reaction.emoji == '1⃣'):
        if(cfg['catches']['catch_common'] <= 1):
            em = discord.Embed(title=("Are you sure you want to go in debt?"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)
            await bot.add_reaction(bait, '✅')
            await bot.add_reaction(bait, '❌')
            res = await bot.wait_for_reaction(('✅', '❌'), user=ctx.message.author, message=bait)
            await bot.delete_message(bait)

            if (res.reaction.emoji == '✅'):
                cfg['catches']['catch_common'] -= 2
                cfg['items']['bait'] += 1
                em = discord.Embed(title=("Transaction successful"), description="", colour=0x3D3D5D)
                bait = await bot.say(embed=em)

            else:
                em = discord.Embed(title=("Transaction canceled"), description="", colour=0x3D3D5D)
                bait = await bot.say(embed=em)
        else:
            cfg['catches']['catch_common'] -= 2
            cfg['items']['bait'] += 1
            em = discord.Embed(title=("Transaction successful"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)

    elif(res.reaction.emoji == '2⃣'):
        if(cfg['catches']['catch_rare'] > 0):
            cfg['catches']['catch_rare'] -= 1
            cfg['items']['bait'] += 2
            em = discord.Embed(title=("Transaction successful"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)
        else:
            em = discord.Embed(title=("Transaction canceled - U broke"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)


    elif (res.reaction.emoji == '3⃣'):
        if (cfg['catches']['catch_epic'] > 0):
            cfg['catches']['catch_epic'] -= 1
            cfg['items']['bait'] += 4
            em = discord.Embed(title=("Transaction successful"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)
        else:
            em = discord.Embed(title=("Transaction canceled - U broke"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)

    elif (res.reaction.emoji == '4⃣'):
        if (cfg['catches']['catch_legendary'] > 0):
            cfg['catches']['catch_legendary'] -= 1
            cfg['items']['bait'] += 25
            em = discord.Embed(title=("Transaction successful"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)
        else:
            em = discord.Embed(title=("Transaction canceled - U broke"), description="", colour=0x3D3D5D)
            bait = await bot.say(embed=em)

    with open(("fishing/" + str(ctx.message.author.id) + ".yml"), 'w') as ymlfile:
        yaml.dump(cfg, ymlfile, default_flow_style=False)
    return
'''
