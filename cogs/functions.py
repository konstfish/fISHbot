from coinmarketcap import Market
from googletrans import Translator
import urbandictionary as ud
import wikipedia

def statTracker( commandN ):
    f = open("storage/stats.txt", encoding='utf-8')
    statsL = f.readlines()
    i = 0
    for command in statsL:
        i += 1
        if (command == commandN):
            break
    statsL[i] = int(statsL[i]) + 1
    statsL[i] = str(statsL[i]) + "\n"
    statsS = ""
    for command in statsL:
        statsS += str(command)
    f.close()
    f = open("storage/stats.txt", "w+", encoding='utf-8')
    f.write(statsS)
    f.close()
    print(commandN + "file verändert")

def statReturner():
    f = open("storage/stats.txt", encoding='utf-8')
    statsL = f.readlines()
    f.close
    statsL.insert(1, "```")
    statsL.append("```")
    statsS = ""
    for command in statsL:
        statsS += str(command)
    return statsS

def pollFetchData( msg ):
    titel = ""
    optionen = []
    wort = ""
    leng = len(msg)
    i = 0

    titelDa = 0
    while i != leng:
        if (msg[i] == "." and titelDa == 0):
            titel = wort
            titelDa = 1
            wort = ""
            i += 1
        elif (msg[i] == "." and titelDa == 1):
            optionen.append(wort)
            wort = ""
            i += 1
        wort += msg[i]
        i += 1
    optionen.append(wort)
    return titel, optionen

def pollFetchResults( send ):
    f = open("polls.txt", encoding='utf-8')
    resultsL = f.readlines()
    f.close()
    i = 0
    returnja = 1
    for user in resultsL:
        if user == (send + "\n"):
            i += 1
            break
            returnja = 0
        i += 1
    if returnja == 1:
        return str(resultsL[i])
    else:
        return

def coinMarketCap( name ):
    coinmarketcap = Market()
    coin = coinmarketcap.ticker(name, limit=3, convert='EUR')
    coinstr = ""
    coinstr += "💳 Symbol: " + coin[0]["symbol"] + "\n"
    coinstr += "💰 Rank: " + coin[0]["rank"] + "\n"
    coinstr += "💶 Price EUR: €" + coin[0]["price_eur"] + "\n"
    coinstr += "💵 Price USD: $" + coin[0]["price_usd"] + "\n"
    coinstr += "💸 Percent Change 24h: " + coin[0]["percent_change_24h"] + " %\n"
    return coinstr

def translateg( phrase ):
    translator = Translator()
    trans = translator.translate(phrase, dest='en')
    return (trans.text)

def urbanDic( phrase ):
    defs = ud.define(phrase)
    sum = ""
    sum += defs[0].word + "\n"
    sum += defs[0].definition + "\n"
    sum += "```" + defs[0].example + "```"
    return sum

def wikisearch( phrase ):
    wiki = wikipedia.page(phrase)
    ausg = wiki.title
    ausg += "\n```"
    ausg += wiki.summary
    return ausg


def getBar( percent ):
    bar = "["
    j = 0
    while (j < percent):
        bar += "="
        j += 10
    while(j != 100):
        bar += " . "
        j += 10
    bar += "]"
    return bar
