#!/usr/bin/env bash

now=$(date +%d-%m-%Y-%M-%S)

ssh fish@ssh.konst.fish mv discord/fISHbot discord/old_fishbots/fishbot_old_$now
scp -r $HOME/Desktop/fISHbot fish@ssh.konst.fish:/home/fish/discord/
ssh fish@ssh.konst.fish scripts/./startBots.sh
