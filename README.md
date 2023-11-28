# fISHbot

Original branch, contains all the hilariously bad code from 2017. Some of my favorite snippets below:

`pushbot.sh` just scpd the new version to my old server & ran a script to create a new [screen](https://linux.die.net/man/1/screen)

why use if when you can just try
```python
try:
    uname = str(ctx.message.author.id)
    em = discord.Embed(title="Your Current Stats: ", description="", colour=0x3D3D5D)
    with open ("fishing/" + uname + ".yml") as ymlfile:
        cfg = yaml.load(ymlfile)

    # ...

    await self.bot.say(embed=em)
except:
    #make default yml file
    try:
        default = dict(
            catches = dict(
                total_catch = 0,
                catch_common = 0,
                catch_rare = 0,
                catch_epic = 0,
                catch_legendary = 0,
            ),
            items = dict(
                rod_lvl = 1,
                bait = 10,
                ),
            user = dict(
                name = str(ctx.message.author.name),
                level = 1,
                lvl_progress = 0,
            )
        )
        with open(("fishing/" + str(ctx.message.author.id) + ".yml"), "w") as ymlfile:
            yaml.dump(default, ymlfile, default_flow_style=False)
    except:
    # ...
```

determining uptime like intended
```python
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
```

```python
if(True):
    emTmp = discord.Embed(title="Fetching Stats...", description="", colour=0x3D3D5D)
```