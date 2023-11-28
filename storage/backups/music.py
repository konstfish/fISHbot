import asyncio
import discord
from discord.ext import commands
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            #await self.bot.send_message(self.current.channel, 'Now playing' + str(self.current))
            em = discord.Embed(title=('🎵 Now playing' + str(self.current)), description="", colour=0x3D3D5D)
            #await self.bot.say(embed=em)
            await self.bot.send_message(self.current.channel, embed=em)
            self.current.player.start()
            await self.play_next_song.wait()
class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        """Summons the bot to join your voice channel."""
        await self.bot.send_typing(ctx.message.channel)
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            em = discord.Embed(title="Nice channel you are in right now.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)
        em = discord.Embed(title=("Moved to " + str(summoned_channel)), description="", colour=0x3D3D5D)
        await self.bot.say(embed=em)
        #variables = status.__dict__.keys()
        #print(str(variables))
        #print(str(status.current))
        #print(str(status.voice.channel))
        #print(str(status.bot))
        #print(str(status.songs))
        #print(str(self.get_voice_state(ctx.message.server))
        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str=None):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """

        await self.bot.send_typing(ctx.message.channel)

        if ctx.message.author.voice_channel is None:
            em = discord.Embed(title="Nice channel you are in right now.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return False

        if(song == None):
            em = discord.Embed(title="You need to put in a song as well tho", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        status = self.get_voice_state(ctx.message.server)
        if(str(status.voice.channel) != (str(ctx.message.author.voice_channel))):
            em = discord.Embed(title="You need to be in the channel to do that.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            await self.bot.say("Loading the song please be patient..")
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.4
            entry = VoiceEntry(ctx.message, player)
            em = discord.Embed(title=('Enqueued ' + str(entry)), description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int = None):
        """Sets the volume of the currently playing song."""

        await self.bot.send_typing(ctx.message.channel)

        if ctx.message.author.voice_channel is None:
            em = discord.Embed(title="Nice channel you are in right now.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return False

        status = self.get_voice_state(ctx.message.server)
        if(str(status.voice.channel) != (str(ctx.message.author.voice_channel))):
            em = discord.Embed(title="You need to be in the channel to do that.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        if (value == None):
            em = discord.Embed(title="Volume missing", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            em = discord.Embed(title=('Set the volume to {:.0%}'.format(player.volume)), description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
        else:
           em = discord.Embed(title="Not playing any music right now!", description="", colour=0x3D3D5D)
           await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """

        await self.bot.send_typing(ctx.message.channel)

        if ctx.message.author.voice_channel is None:
            em = discord.Embed(title="Nice channel you are in right now.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return False

        status = self.get_voice_state(ctx.message.server)
        if(str(status.voice.channel) != (str(ctx.message.author.voice_channel))):
            em = discord.Embed(title="You need to be in the channel to do that.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            em = discord.Embed(title="Cleared the queue and disconnected from voice channel ", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):

        await self.bot.send_typing(ctx.message.channel)

        if ctx.message.author.voice_channel is None:
            em = discord.Embed(title="Nice channel you are in right now.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return False

        status = self.get_voice_state(ctx.message.server)
        if(str(status.voice.channel) != (str(ctx.message.author.voice_channel))):
            em = discord.Embed(title="You need to be in the channel to do that.", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            em = discord.Embed(title="No music playing right now...", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            return
        else:
            em = discord.Embed(title='Skipping song...', description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
            state.skip()

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            em = discord.Embed(title="No music playing right now...", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)
        else:
            skip_count = len(state.skip_votes)
            em = discord.Embed(title="cba bruh", description="", colour=0x3D3D5D)
            await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Music(bot))
    print('Music bot live')
