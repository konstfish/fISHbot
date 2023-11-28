import os
import datetime

def mailme(err, id, ctx):

    now = datetime.datetime.now()
    date = now.strftime("%d.%m")
    time = now.strftime("%H:%M")

    msgdata = ("Sent by: @" + str(ctx.message.author) + "\nServer: " + str(ctx.message.server) + "\nChannel: " + str(ctx.message.channel) + "\nContent: " + str(ctx.message.content)  + "\nError: ")

    command = ("echo '" + msgdata + err + "'")
    command += (" | mutt -s 'fISHbot error from the " + date + " at " + time + ". ID: " + id + "' david.fishical@gmail.com")

    os.system(str(command))
    print("Email deployed boys")
