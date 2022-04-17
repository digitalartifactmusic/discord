import random
from urllib.request import urlopen
from attr import attrib
import discord
import math
from discord.client import Client
from discord.ext.commands.bot import Bot
from discord.message import Message
from google_images_search.fetch_resize_save import FetchResizeSave
import requests
from discord import Permissions
from discord.ext import commands
from discord.utils import get
from collections import defaultdict
from discord import FFmpegPCMAudio
from discord.utils import get
from PIL import Image
import numpy as np
import shutil
import os
import asyncio
import itertools
from functools import partial
import math
import random
from async_timeout import timeout
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.voice_client import AudioPlayer
from sclib import SoundcloudAPI, Track, Playlist
from sclib import sync
from bs4 import BeautifulSoup
import urllib3
import requests
import coverpy
from google_images_search import GoogleImagesSearch
import sys
import pprint
import yt_dlp
import time
import json
import difflib
import re
import urllib
import lyricsgenius

# def manipulateparse(code: str):
#     temp = ''
#     for i in code:

class Message:
    def __init__(self, snipe: str, *, data: discord.Message):
        self.data = data
        self.snipe = snipe

messagehistory = defaultdict(lambda: defaultdict(list))

helppages = []

embed=discord.Embed(title="revive bot Guide", description="Basic Music Commands", color = discord.Color.random())
embed.set_author(name="revive Bot", url="https://ybtv.cloud/", icon_url="https://i.ibb.co/6b3ZbK0/Studio-Project.png")
embed.add_field(name="r!setup", value="Creates a yb-Bot channel and a DJ role. Do r!givedj @user to give DJ role.", inline=False)
embed.add_field(name="r!play", value="Tries to play music from a link or search query.\nr!p data.matrix ryoji ikeda\nr!p https://open.spotify.com/playlist/5y8vxajDigqqiIFbgiBWa0?si=09c941ff9d844cf6\n(Officially supports Spotify, Soundcloud, YouTube)\n", inline=False)
embed.add_field(name="r!queue", value="Displays the current music queue.\nr!q", inline=False)
embed.add_field(name="r!skip", value="Skips to some point in the queue.\nr!s (Skips currently playing song)\nr!s 10 (Skips to position 10 in queue)\nr!s 123 (Clears queue if outside queue range)", inline=False)
embed.add_field(name="r!movefront", value="Moves the given queue position to the front.\nr!mf 14", inline=False)
embed.add_field(name="r!remove", value="Removes the given queue position.\nr!remove 14", inline=False)
embed.add_field(name="r!shuffle", value="Shuffles the current queue.\nr!sh", inline=False)
embed.add_field(name="r!lyrics", value="Shows the lyrics for the currently playing song.\nr!lyr\n(Powered by Genius API)\n", inline=False)
embed.add_field(name="r!loop", value="Loops and unloops the currently playing track.\nr!l\n", inline=False)
embed.set_footer(text="Made by Digital Artifact#5352")

helppages.append(embed)

embed=discord.Embed(title="revive bot Guide", description="Advanced Music Commands", color = discord.Color.random())
embed.set_author(name="revive Bot", url="https://ybtv.cloud/", icon_url="https://i.ibb.co/6b3ZbK0/Studio-Project.png")
embed.add_field(name="r!pause", value="Pauses yb Bot.", inline=False)
embed.add_field(name="r!unpause", value="Unpauses yb Bot", inline=False)
embed.add_field(name="r!clear", value="Clears the current music queue", inline=False)
embed.add_field(name="r!back", value="Adds previously played song to front of queue.", inline=False)
embed.add_field(name="r!dj <role_name>", value="Creates DJ role with that name.", inline=False)
embed.add_field(name="r!renamedj <role_name>", value="Renames current DJ role.", inline=False)
embed.add_field(name="r!givedj @user", value="Gives user current DJ role.", inline=False)
embed.add_field(name="r!setdj @role", value="Sets current DJ role to given role.", inline=False)
embed.add_field(name="r!history", value="Shows server history\nr!history play -6 (Plays that song in the last history queue)", inline=False)
embed.add_field(name="r!userhistory", value="Shows user history\nr!userhistory (Displays your user history)\nr!userhistory @user (Displays that users history)\nr!history play -6 (Plays that song in the last history queue)", inline=False)
embed.add_field(name="(Admin Only) r!lock", value="Locks yb Bot.", inline=False)
embed.add_field(name="(Admin Only) r!unlock", value="Unlocks yb Bot.", inline=False)
embed.add_field(name="(Admin Only) r!kill", value="Kills current yb Bot process in your server.", inline=False)
embed.set_footer(text="Made by Digital Artifact#5352")

helppages.append(embed)

embed=discord.Embed(title="revive bot Guide", description="Server Building Commands", color = discord.Color.random())
embed.set_author(name="revive Bot", url="https://ybtv.cloud/", icon_url="https://i.ibb.co/6b3ZbK0/Studio-Project.png")
embed.add_field(name="r!colorgenerate", value="r!cg <start_hex> <end_hex> <list of roles>\nr!cg db42a0 7a0000 01 02 03 04 05 'temporal anomaly' 06 (Creates the given list of roles with the given gradient)\nr!cg db42a0 7a0000 @role @role @role ... \n(Recolors the given list of roles with the given gradient)", inline=False)
embed.add_field(name="r!deleteroles", value="r!del <list_of_roles>\nr!del 01 02 03 04 05 'temporal anomaly' 06\nr!del @role @role @role...\n(Deletes the given list of roles)", inline=False)
embed.add_field(name="r!moveroles", value="r!mr <role_to_move_above> 01 03 04 'temporal anomaly' 06\nr!mr @role_to_move_above @role @role @role...\n(Moves the given list of roles above the move above role)", inline=False)
embed.add_field(name="r!generateroleemote", value="r!emote circle 01 02 03 04 05 'temporal anomaly' t1 t2 t3 t4 t5 @role ...\n(Generates a ZIP of the given role list colors in the shape specified)\n(Current supported shapes are circle, heart)", inline=False)
embed.add_field(name="r!renameroles", value="r!rr 01 02 03 04 05 'temporal anomaly' t1 t2 t3 t4 t5 'test bot'\n(Renames 6 roles)\nr!rr @role @role @role @role @role @role\n(Renames 3 roles)", inline=False)
embed.add_field(name="r!undo", value="r!u (Undoes the last thing having to do with role management.)\nr!u 5 (Undoes the last 5 things having to do with role management.)", inline=False)
embed.set_footer(text="Made by Digital Artifact#5352")

helppages.append(embed)

embed=discord.Embed(title="revive bot Guide", description="Fun Commands", color = discord.Color.random())
embed.set_author(name="revive Bot", url="https://ybtv.cloud/", icon_url="https://i.ibb.co/6b3ZbK0/Studio-Project.png")
embed.add_field(name="r!textcomplete", value="r!tc <prompt>\n(Takes the beginning of a story and tries to write more)\n(Powered by GPT-2 under Inferkit API)", inline=False)
embed.add_field(name="Much more to come!", value=" ... ", inline=False)
embed.set_footer(text="Made by Digital Artifact#5352")

helppages.append(embed)

embed=discord.Embed(title="revive bot Guide", description="Utility Commands", color = discord.Color.random())
embed.set_author(name="revive Bot", url="https://ybtv.cloud/", icon_url="https://i.ibb.co/6b3ZbK0/Studio-Project.png")
embed.add_field(name="r!avatar", value="r!av\nr!av @user\n(Shows list of user avatars)", inline=False)
embed.add_field(name="r!banner", value="\n(Shows user banner)", inline=False)
embed.add_field(name="r!prefix", value="r!prefix <list_of_prefixes>\nr!prefix !\n(Changes prefix to list of prefixes)", inline=False)
embed.add_field(name="r!snipe", value="r!snipe\n(Shows last 100 deleted messages)", inline=False)
embed.add_field(name="Much more to come!", value=" ... ", inline=False)
embed.set_footer(text="Made by Digital Artifact#5352")

helppages.append(embed)


covergetter = coverpy.CoverPy()

useragent  = 'yb 1.32'

customprefixes = json.load(open('data/customprefixes.json'))
undoroster = json.load(open('data/undoroster.json'))
rolesdeleted = json.load(open('data/rolesdeleted.json'))
rolescreated = json.load(open('data/rolescreated.json'))
lastonehundredmessages = json.load(open('data/lastonehundredmessages.json'))
userspotifylikedtracks = json.load(open('data/userspotifylikedtracks.json'))
serverhistory = json.load(open('data/serverhistory.json'))
serverchannel = json.load(open('data/serverchannel.json'))
userhistory = json.load(open('data/userhistory.json'))
dj = json.load(open('data/dj.json'))

loop = asyncio.get_event_loop()

async def dump_periodically():
    while True:
        json.dump(lastonehundredmessages, open('data/lastonehundredmessages.json', 'w'))
        json.dump(undoroster, open('data/undoroster.json', 'w'))
        json.dump(customprefixes, open('data/customprefixes.json', 'w'))
        json.dump(rolescreated, open('data/rolescreated.json', 'w'))
        json.dump(rolesdeleted, open('data/rolesdeleted.json', 'w'))
        json.dump(serverhistory, open('data/serverhistory.json', 'w'))
        json.dump(serverchannel, open('data/serverhistory.json', 'w'))
        json.dump(userhistory, open('data/userhistory.json', 'w'))
        json.dump(userspotifylikedtracks, open('data/userspotifylikedtracks.json', 'w'))
        json.dump(dj, open('data/dj.json', 'w'))
        await asyncio.sleep(20)

loop.create_task(dump_periodically())

palettes = []
previoushistory = {}
#palettenameandnumber = defaultdict(str)

defaultprefixes = ['r!']

# Sensitive information.

googleimagesearch = GoogleImagesSearch(googleclientid, googleimagesearchid)

clientcredentialsmanager = SpotifyClientCredentials(client_id = spotifyclientid, client_secret = spotifyclientsecret)
spotify = spotipy.Spotify(client_credentials_manager = clientcredentialsmanager)

soundcloud = SoundcloudAPI(soundcloudclientid)

genius = lyricsgenius.Genius(geniustoken)

YTDL_OPTIONS = {
        'format': 'bestaudio/best/mp3',
        'audioquality': '48K',
        'extractaudio': True,
        'audioformat': 'best/mp3',
        'keepvideo': False,
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
youtubedownload = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.FFmpegPCMAudio, *, data, volume = 0.3, requester):
        super().__init__(source, volume)
        self.data = data
        self.requester = requester

        self.type = data.get('type')

        self.title = data.get('title')
        self.artwork_url = data.get('artwork_url')
        self.artist = data.get('artist')

        self.lyrics = None

        self.weburl = data.get('webpage_url')

        if 'recommended' in data:
            self.recommended = data.get('recommended')
        else:
            self.recommended = False

class MusicPlayer:
    def __init__(self, ctx):
        self.context = ctx
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.cog = ctx.cog
        self.looptrack = False

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.source = None
        self.currentsource = None

        self.skipvotes = set()

        self.locked = False
        self.lockrequester = ''

        ctx.bot.loop.create_task(self.audio_player())

    async def audio_player(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            if str(self.guild.id) in serverchannel:
                self.channel = serverchannel[str(self.guild.id)]

            try:
                async with timeout(300):
                    self.source = await self.queue.get()
            except:
                print('Destroying.')
                return self.destroy(self.guild)

            try:
                requester = self.bot.get_user(id = self.source['requester'])
            except:
                await self.channel.send(f"Requester dissapeared.")
                continue

            if self.source['type'] == 'spotify':
                # Get info for spotify track. Search soundcloud first, if not a close match fall back on yt-dlp automation.
                track = spotify.track(self.source['trackuri'])

                spotifytitle = re.sub('[:.\-+[\]]+', ' ', self.source["title"])
                spotifyartist = re.sub('[:.\-+[\]]+', ' ', self.source["artist"])

                webpage = f'{spotifytitle} {spotifyartist}' 
                self.source['artwork_url'] = track['album']['images'][0]['url']

                if not 'recommended' in self.source:
                    if str(requester.id) in userspotifylikedtracks:
                        userspotifylikedtracks[str(requester.id)].append(self.source['trackuri'])
                    else:
                        userspotifylikedtracks[str(requester.id)] = [self.source['trackuri']]

                try:
                    soundcloudobject = soundcloud.search(webpage.replace(' ', '%20'))
                    soundcloudtitle = re.sub('[:.\-+[\]]+', ' ', soundcloudobject.title)
                    soundcloudartist = re.sub('[:.\-+[\]]+', ' ', soundcloudobject.artist)
                    if soundcloudobject:
                        soundcloudvsspotify = difflib.SequenceMatcher(None, f'{soundcloudtitle} {soundcloudartist}', webpage).ratio()
                            
                        if not soundcloudvsspotify > 0.5:
                            raise Exception()

                        webpage = soundcloudobject.permalink_url
                    else:
                        raise Exception()
                except:
                    pass
            elif self.source['type'] == 'soundcloud':
                soundcloudtitle = re.sub('[:.\-+[\]]+', ' ', self.source['title'])
                soundcloudartist = re.sub('[:.\-+[\]]+', ' ', self.source['artist'])

                if self.source['webpage_url']:
                    webpage = self.source['webpage_url']
                else:
                    webpage = f'{soundcloudtitle} {soundcloudartist}'

                if str(self.guild.id) in serverchannel:
                    self.channel = serverchannel[str(self.guild.id)]
                
                try:
                    uri = spotify.search(f'{soundcloudtitle} {soundcloudartist}', limit = 1)['tracks']['items'][0]['uri']
                    spotifyobject = spotify.track(uri)
                    spotifytitle = re.sub('[:.\-+[\]]+', ' ', spotifyobject["name"])
                    spotifyartist = re.sub('[:.\-+[\]]+', ' ', spotifyobject["artists"][0]["name"])

                    soundcloudvsspotify = difflib.SequenceMatcher(None, f'{soundcloudtitle} {soundcloudartist}', f'{spotifytitle} {spotifyartist}').ratio()

                    if not soundcloudvsspotify > 0.5:
                        if str(requester.id) in userspotifylikedtracks:
                            userspotifylikedtracks[str(requester.id)].append(uri)
                        else:
                            userspotifylikedtracks[str(requester.id)] = [uri]
                except:
                    pass

                self.source['artwork_url'] = 'https://i1.sndcdn.com/artworks-' + '-'.join(str(self.source['artwork_url']).split('-')[-3:-1]) + '-t500x500.jpg'
            else:
                webpage = self.source['webpage_url']

                self.source['search'] = re.sub('[:.\-+[\]]+', ' ', self.source['search'])
                title = re.sub('[:.\-+[\]]+', ' ', self.source['title'])

                try: 
                    try:
                        uri = spotify.search(self.source['search'], limit = 1)['tracks']['items'][0]['uri']
                    except:
                        uri = spotify.search(title, limit = 1)['tracks']['items'][0]['uri']
                    spotifyobject = spotify.track(uri)

                    spotifytitle = re.sub('[:.\-+[\]]+', ' ', spotifyobject["name"])
                    spotifyartist = re.sub('[:.\-+[\]]+', ' ', spotifyobject["artists"][0]["name"])

                    spotifyvssearch = difflib.SequenceMatcher(None, f'{spotifytitle} {spotifyartist}', title).ratio()

                    if spotifyvssearch > 0.5:
                        self.source['artist'] = spotifyartist
                        self.source['artwork_url'] = spotifyobject['album']['images'][0]['url']

                        if str(requester.id) in userspotifylikedtracks:
                            userspotifylikedtracks[str(requester.id)].append(uri)
                        else:
                            userspotifylikedtracks[str(requester.id)] = [uri]
                except:
                    spotifytitle = None
                    spotifyartist = None

                try:
                    if spotifytitle:
                        soundcloudobject = soundcloud.search(str(f'{spotifytitle} {spotifyartist}').replace(' ', '%20'))
                    else:
                        try:
                            soundcloudobject = soundcloud.search(self.source['search'].replace(' ', '%20'))
                        except:
                            soundcloudobject = soundcloud.search(title.replace(' ', '%20'))

                    if soundcloudobject:
                        soundcloudtitle = re.sub('[:.\-+[\]]+', ' ', soundcloudobject.title) 
                        soundcloudartist = re.sub('[:.\-+[\]]+', ' ', soundcloudobject.artist)

                        soundcloudvssearch = difflib.SequenceMatcher(None, f'{soundcloudtitle} {soundcloudartist}', self.source['search']).ratio()
                            
                        if spotifytitle:
                            if not difflib.SequenceMatcher(None, f'{spotifytitle} {spotifyartist}' f'{soundcloudtitle} {soundcloudartist}').ratio() > 0.5:
                                if not soundcloudvssearch > 0.5:
                                    raise Exception()
                        else:
                            if not soundcloudvssearch > 0.5:
                                raise Exception()

                        webpage = soundcloudobject.permalink_url
                        self.source['title'] = soundcloudtitle
                        self.source['artist'] = soundcloudartist

                        if soundcloudobject.artwork_url:
                            self.source['artwork_url'] = 'https://i1.sndcdn.com/artworks-' + '-'.join(str(soundcloudobject.artwork_url).split('-')[-3:-1]) + '-t500x500.jpg'
                        else:
                            if not self.source['artwork_url']:
                                raise Exception()
                    else:
                        raise Exception()
                except:
                    try:
                        if '.com' in self.source['search']:
                            if spotifyartist:
                                self.source['artwork_url'] = covergetter.get_cover(f'{title} {spotifyartist}', 1).artwork(500)
                            else:
                                self.source['artwork_url'] = covergetter.get_cover(f'{title}', 1).artwork(500)
                        else:
                            self.source['artwork_url'] = covergetter.get_cover(f'{title}', 1).artwork(500)
                    except:
                        if '.com' in self.source["search"]:
                            if spotifyartist:
                                googleimagesearch.search({'q': f'{title} {spotifyartist} cover art', 'num': 1, 'fileType': 'jpg'})
                                self.source['artwork_url'] = googleimagesearch.results()[0].url
                            else:
                                googleimagesearch.search({'q': f'{title} cover art', 'num': 1, 'fileType': 'jpg'})
                                self.source['artwork_url'] = googleimagesearch.results()[0].url
                        else:
                            googleimagesearch.search({'q': f'{title} cover art', 'num': 1, 'fileType': 'jpg'})
                            self.source['artwork_url'] = googleimagesearch.results()[0].url

            if not '.com' in webpage:
                data = await self.bot.loop.run_in_executor(None, lambda: youtubedownload.extract_info(url = webpage, download = False))
                if 'entries' in data:
                    download = await self.bot.loop.run_in_executor(None, lambda: youtubedownload.extract_info(url = data['entries'][0]['webpage_url'], download = True))
                else:
                    download = await self.bot.loop.run_in_executor(None, lambda: youtubedownload.extract_info(url = data['webpage_url'], download = True))
            else:
                download = await self.bot.loop.run_in_executor(None, lambda: youtubedownload.extract_info(url = webpage, download = True))

            file = youtubedownload.prepare_filename(download)
            
            self.currentsource = YTDLSource(discord.FFmpegPCMAudio(file), data = self.source, requester = requester)

            self.guild.voice_client.play(self.currentsource, after = lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            
            try:
                format = f'`{self.currentsource.title}` by `{self.currentsource.artist}` \nRequested by: 'f'`{self.currentsource.requester}`'
                embed = discord.Embed(title=f'Now Playing:', description = format, colour = discord.Colour.random())
                embed.set_image(url = f'{self.currentsource.artwork_url}')
                message = await self.channel.send(embed = embed)
            except:
                await self.channel.send(f"Could not make now playing embed.")
                pass
                
            await self.next.wait()

            if str(self.guild.id) in serverhistory:
                serverhistory[str(self.guild.id)].insert(0, self.source)
            else:
                serverhistory[str(self.guild.id)] = [self.source]

            if str(requester.id) in userhistory:
                userhistory[str(requester.id)].insert(0, self.source)
            else:
                userhistory[str(requester.id)] = [self.source]

            self.currentsource.cleanup()

            try:
                os.remove(file)
            except:
                pass

            try:
                await message.delete()
            except:
                pass

            print(f'Cleaning... {time.strftime("%H:%M:%S", time.localtime())} {self.currentsource.title}')
            self.currentsource = None

            if self.looptrack:
                self.queue._queue.insert(0, self.source)

    async def move_front(self, position: int):
        temp = self.queue._queue[position]
        del self.queue._queue[position]
        self.queue._queue.insert(0, temp)
        return

    async def back(self):
        if str(self.guild.id) in serverhistory:
            self.queue._queue.insert(0, serverhistory[str(self.guild.id)][0])
            await self.channel.send(f"Operation successfully performed!")
        else:
            await self.channel.send(f"There is no history for your server.")
        return

    async def skip(self, amount: int):
        for i in range(amount):
            del self.queue._queue[0]
        return

    async def shuffle(self):
        random.shuffle(self.queue._queue)
        return

    async def remove(self, position: int):
        del self.queue._queue[position]
        return

    def destroy(self, guild):
        return self.bot.loop.create_task(self.cog.cleanup(guild))

players = defaultdict(MusicPlayer)
playroster = {}

class Music(commands.Cog):
    def __init__(self, yb: commands.Bot):
        self.bot = yb
        self.bot.loop = loop

    async def cleanup(self, guild: discord.Guild):
        if guild.voice_client:
            await guild.voice_client.disconnect()

        del players[guild.id]

    async def checkadministrator(self, ctx: commands.Context):
        if ctx.message.author.guild_permissions.administrator:
            return True
        else:
            await ctx.send('You need admin for that...')
            return False

    async def checkmanageroles(self, ctx: commands.Context):
        if ctx.message.author.guild_permissions.manage_roles:
            return True
        else:
            await ctx.send('You need admin for that...')
            return False

    async def checkdj(self, ctx: commands.Context):
        if str(ctx.message.guild.id) in dj:
            if not get(ctx.message.guild.roles, id = dj[str(ctx.message.guild.id)]) in ctx.message.guild.get_member(ctx.message.author.id).roles:
                await ctx.message.channel.send('You need dj role to do that.')
                return False
            else:
                return True
        else:
            await ctx.message.channel.send(f"You need dj role to do that, there is currently not a dj role for your server.")
            return False

    async def checklocked(self, ctx: commands.Context):
        if ctx.guild.id in players:
                if players[ctx.guild.id].locked:
                    await ctx.send(f"yb bot music functionality is currently locked by administrator {self.lockrequester[ctx.guild.id]}! Ask an administrator to unlock the bot for your access.")
                    return True
                else:
                    return False
        else:
            await ctx.send(f"There are currently no yb bot player instances running in your server.")
            return True

    async def connect(self, ctx: commands.Context):
        if ctx.message.author.voice:
            if ctx.message.guild.voice_client:
                if not (ctx.message.author.voice.channel == ctx.message.guild.voice_client.channel):
                    if ctx.message.author.guild_permissions.administrator:
                        await ctx.message.guild.voice_client.move_to(ctx.message.author.voice.channel)
                        return True
                    await ctx.message.channel.send('You must be in the voice chat with yb bot...')
                    return False
                else:
                    return True
            else:
                await ctx.message.author.voice.channel.connect()
                return True
        else:
            await ctx.message.channel.send(f"You must join a voice channel to invite yb bot!")
            return False

    async def getsoundcloudinfourl(self, ctx: commands.Context, url: str):
        split = url.split('/')
        if split[0] == 'https:':
            del split[0]
            del split[0]

        if not len(split) > 2:
            await ctx.message.channel.send('Unsupported soundcloud link!')
            return False

        try:
            soundcloudobject = soundcloud.resolve(url)
        except:
            await ctx.message.channel.send('Unsupported soundcloud link!')
            return False

        if split[2] == 'sets':
            if type(soundcloudobject) == Playlist:
                size = len(soundcloudobject.tracks)
                await ctx.message.channel.send(f'```ini\n[Adding {size} songs to the Queue.]\n```', delete_after = 15)
                for track in soundcloudobject.tracks:
                    if track.monetization_model == 'SUB_HIGH_TIER':
                        await players[ctx.message.guild.id].queue.put({
                            'webpage_url': None,
                            'requester': ctx.message.author.id,
                            'title': track.title,
                            'artist': track.artist,
                            'artwork_url': track.artwork_url,
                            'type': 'soundcloud'})
                    else:
                        await players[ctx.message.guild.id].queue.put({
                            'webpage_url': track.permalink_url,
                            'requester': ctx.message.author.id,
                            'title': track.title,
                            'artist': track.artist,
                            'artwork_url': track.artwork_url,
                            'type': 'soundcloud'})
            else:
                await ctx.message.channel.send('Unsupported soundcloud link!')
                return False
        else:
            if type(soundcloudobject) == Track:
                await ctx.message.channel.send(f'```ini\n[Adding 1 song to the Queue.]\n```', delete_after = 15)
                if soundcloudobject.monetization_model == 'SUB_HIGH_TIER':
                    await players[ctx.message.guild.id].queue.put({
                        'webpage_url': None,
                        'requester': ctx.message.author.id, 
                        'title': soundcloudobject.title, 
                        'artist': soundcloudobject.artist,
                        'artwork_url': soundcloudobject.artwork_url,
                        'type': 'soundcloud'})
                else:
                    await players[ctx.message.guild.id].queue.put({
                        'webpage_url': soundcloudobject.permalink_url, 
                        'requester': ctx.message.author.id, 
                        'title': soundcloudobject.title, 
                        'artist': soundcloudobject.artist,
                        'artwork_url': soundcloudobject.artwork_url,
                        'type': 'soundcloud'})
            else:
                await ctx.message.channel.send('Unsupported soundcloud link!')
                return False
        
        return True

    async def getspotifyinfourl(self, ctx: commands.Context, url: str):
        split = url.split('/')

        if split[0] == 'https:':
            del split[0]
            del split[0]

        if not len(split) == 3:
            await ctx.message.channel.send('Unsupported spotify link!')
            return False

        uri = split[-1].split('?')[0]
        mediatype = split[-2]
        
        if mediatype == 'playlist':
            size = len(spotify.playlist_tracks(uri)['items'])
            await ctx.message.channel.send(f'```ini\n[Adding {size} songs to the Queue.]\n```', delete_after = 15)
            for spotifyobject in spotify.playlist_tracks(uri)['items']:
                await players[ctx.message.guild.id].queue.put({
                    'requester': ctx.message.author.id, 
                    'title': spotifyobject["track"]["name"],  
                    'artist': spotifyobject["track"]["artists"][0]["name"], 
                    'trackuri': spotifyobject['track']['uri'], 
                    'type': 'spotify'})
        elif mediatype == 'track':
            spotifyobject = spotify.track(uri)
            await ctx.send(f'```ini\n[Adding 1 song to the Queue.]\n```', delete_after = 15)
            await players[ctx.message.guild.id].queue.put({
                'requester': ctx.message.author.id, 
                'title': spotifyobject["name"], 
                'artist': spotifyobject["artists"][0]["name"], 
                'trackuri': uri,
                'type': 'spotify'})
        elif mediatype == 'artist':
            size = len(spotify.artist_top_tracks(uri)["tracks"])
            await ctx.send(f'```ini\n[Adding {size} songs to the Queue.]\n```', delete_after = 15)
            for spotifyobject in spotify.artist_top_tracks(uri)["tracks"]:
                await players[ctx.message.guild.id].queue.put({
                    'requester': ctx.message.author.id, 
                    'title': spotifyobject["name"], 
                    'artist': spotifyobject["artists"][0]["name"], 
                    'trackuri': spotifyobject["uri"],
                    'type': 'spotify'})
        elif mediatype == 'album':
            size = len(spotify.album_tracks(uri)["items"])
            await ctx.send(f'```ini\n[Adding {size} songs to the Queue.]\n```', delete_after = 15)
            for spotifyobject in spotify.album_tracks(uri)["items"]:
                await players[ctx.message.guild.id].queue.put({
                    'requester': ctx.message.author.id, 
                    'title': spotifyobject["name"], 
                    'artist': spotifyobject["artists"][0]["name"], 
                    'trackuri': spotifyobject["uri"],
                    'type': 'spotify'})
        else:
            await ctx.message.channel.send('Unsupported spotify link!')
            return False

        return True

    @commands.command()
    async def dj(self, ctx: commands.Context, *, rolename: str = "DJ"):
        """yb.dj <Optional: role name>, creates default dj role"""
        if not await self.bot.loop.create_task(self.checkmanageroles(ctx)):
            return

        if str(ctx.message.guild.id) in dj:
            await ctx.message.channel.send(f'There is already a dj role for your server!')
            return

        role = await ctx.message.guild.create_role( name = rolename , color = discord.Colour.blue() )

        dj[str(ctx.message.guild.id)] = role.id

        await ctx.message.channel.send(f'Successfully created role {rolename} as the dj role, you can assign people this role to control who has access to some bot functions...')

        return

    @commands.command(aliases = ["gdj"])
    async def givedj(self, ctx: commands.Context, user: discord.Member = None):
        """yb.gdj <@user>, assigns server dj role"""
        if not await self.bot.loop.create_task(self.checkmanageroles(ctx)):
            return

        if not user:
            await ctx.message.channel.send('Please specify a user to add the dj role to...')
            return

        if not str(ctx.message.guild.id) in dj:
            await ctx.message.channel.send('There is currently no dj role for your server. If you are admin, you can make one using yb.dj.')

        await user.add_roles(get(ctx.message.guild.roles, id = dj[str(ctx.message.guild.id)]))

        await ctx.message.channel.send(f'Successfully gave user {user} dj role...')

        return

    @commands.command(aliases = ["sdj"])
    async def setdj(self, ctx: commands.Context, role: discord.Role = None):
        """yb.gdj <@user>, assigns server dj role"""
        if not await self.bot.loop.create_task(self.checkmanageroles(ctx)):
            return

        dj[str(ctx.message.guild.id)] = role.id

        await ctx.message.channel.send(f'Successfully set {role.name} as yb bot dj role...')

        return
    
    @commands.command(aliases = ["rdj"])
    async def renamedj(self, ctx: commands.Context, *, rolename: str = None):
        """yb.gdj <@user>, assigns server dj role"""
        if not await self.bot.loop.create_task(self.checkmanageroles(ctx)):
            return

        if not str(ctx.message.guild.id) in dj:
            await ctx.message.channel.send('There is currently no dj role for your server. If you are admin, you can make one using yb.dj.')

        djrole = get(ctx.message.guild.roles, id = dj[str(ctx.message.guild.id)])

        try:
            await djrole.edit(name = rolename, reason = None)
        except:
            await ctx.message.channel.send(f'Couldn\'t rename DJ role... Make sure ybtv2 role is above the DJ role!')
            return

        await ctx.message.channel.send(f'Successfully ranamed dj role to {rolename}...')

        return

    @commands.command(aliases = ["set"])
    async def setup(self, ctx: commands.Context):
        """yb.gdj <@user>, assigns server dj role"""
        try:
            channel = next((x for x in ctx.message.guild.text_channels if x.name == 'yb-bot'), None)
        except:
            channel = await ctx.message.guild.create_text_channel('yb-bot')

        if str(ctx.message.guild.id) in dj:
            await channel.send(f'There is a dj role for your server, you can use yb.givedj @user or yb.renamedj <role_name>. Do yb.help for all commands.')
        else:
            if not await self.bot.loop.create_task(self.checkmanageroles(ctx)):
                return

            role = await ctx.message.guild.create_role( name = 'DJ' , color = discord.Colour.blue() )

            dj[str(ctx.message.guild.id)] = role.id

            await channel.send('DJ role have been created, you can use yb.givedj @user or yb.renamedj <role_name>. Do yb.help for all commands.')

        currentchunk = 0
        message = await channel.send(embed = helppages[currentchunk])

        try:
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')
        except:
            await message.channel.send('yb Bot needs reaction add permissions to add pages to the help message')

        def check(reaction, user):
            return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)

        while True:
            try:
                reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 300)
            except asyncio.TimeoutError:
                return
                
            if str(reaction.emoji) == "➡️":
                if currentchunk == len(helppages) - 1:
                    currentchunk = 0
                else:
                    currentchunk += 1

                await message.edit(embed = helppages[currentchunk])

                await reaction.remove(author)

            if str(reaction.emoji) == "⬅️":
                if currentchunk == 0:
                    currentchunk = len(helppages) - 1
                else:
                    currentchunk -= 1

                await message.edit(embed = helppages[currentchunk])
            
                await reaction.remove(author)

    @commands.command(aliases = ["p"])
    async def play(self, ctx: commands.Context, *, search: str):
        """yb.p <search>, supports most urls and search terms"""
        if not await self.bot.loop.create_task(self.connect(ctx)):
            return
        
        if ctx.message.guild.id in playroster:
            if playroster[ctx.message.guild.id]:
                playroster[ctx.message.guild.id].append(tuple((ctx, search, '')))
                await ctx.message.channel.send('yb bot is currently busy, probably queueing a really big playlist! Adding your query after the current one.')
                return
            else:
                playroster[ctx.message.guild.id] = [tuple((ctx, search, ''))]
        else:
            playroster[ctx.message.guild.id] = [tuple((ctx, search, ''))]
            
        while(playroster[ctx.message.guild.id]):
            ctx = playroster[ctx.message.guild.id][0][0]
            search = playroster[ctx.message.guild.id][0][1]

            async with ctx.message.channel.typing():
                if ctx.message.guild.id in players:
                    player = players[ctx.message.guild.id]
                else:
                    player = MusicPlayer(ctx)
                    players[ctx.message.guild.id] = player

                if 'spotify.com/' in search:
                    temp = await self.bot.loop.create_task(self.getspotifyinfourl(ctx, search))
                    if not temp:
                        await ctx.message.channel.send('Something went wrong. :(')
                    del playroster[ctx.message.guild.id][0]
                    continue

                if 'soundcloud.com/' in search:
                    temp = await self.bot.loop.create_task(self.getsoundcloudinfourl(ctx, search))
                    if not temp:
                        await ctx.message.channel.send('Something went wrong. :(')
                    del playroster[ctx.message.guild.id][0]
                    continue


                if '.com' in search:
                    try:
                        data = await self.bot.loop.run_in_executor(None, lambda: youtubedownload.extract_info(url = search, download = False))
                    except:
                        await ctx.message.channel.send('Something went wrong. :(')
                        del playroster[ctx.message.guild.id][0]
                        continue
                    
                    if 'entries' in data:
                        size = len(data['entries'])
                        await ctx.message.channel.send(f'```ini\n[Adding {size} songs to the Queue.]\n```', delete_after = 15)
                        for i in data['entries']:
                            await player.queue.put({
                                'webpage_url': i['webpage_url'], 
                                'requester': ctx.message.author.id, 
                                'title': i['title'], 
                                'artwork_url': None, 
                                'artist': None,
                                'type': 'yt-dlp',
                                'search': i['title']})
                    else:
                        await ctx.message.channel.send(f'```ini\n[Adding 1 song to the Queue.]\n```', delete_after = 15)
                        await player.queue.put({
                            'webpage_url': data['webpage_url'], 
                            'requester': ctx.message.author.id, 
                            'title': data['title'], 
                            'artwork_url': None, 
                            'artist': None,
                            'type': 'yt-dlp',
                            'search': data['title']})
                else:
                    try:
                        data = await self.bot.loop.run_in_executor(None, lambda: youtubedownload.extract_info(url = search, download = False))
                    except:
                        await ctx.message.channel.send('Something went wrong. :(')
                        del playroster[ctx.message.guild.id][0]
                        continue
                    
                    if 'entries' in data:
                        size = len(data['entries'])
                        await ctx.message.channel.send(f'```ini\n[Adding {size} songs to the Queue.]\n```', delete_after = 15)
                        for i in data['entries']:
                            await player.queue.put({
                                'webpage_url': i['webpage_url'], 
                                'requester': ctx.message.author.id, 
                                'title': i['title'], 
                                'artwork_url': None, 
                                'artist': None,
                                'type': 'yt-dlp',
                                'search': search})
                    else:
                        await ctx.message.channel.send(f'```ini\n[Adding 1 song to the Queue.]\n```', delete_after = 15)
                        await player.queue.put({
                            'webpage_url': data['webpage_url'], 
                            'requester': ctx.message.author.id, 
                            'title': data['title'], 
                            'artwork_url': None, 
                            'artist': None,
                            'type': 'yt-dlp',
                            'search': search})
                    
                del playroster[ctx.message.guild.id][0]
        return

    @commands.command()
    async def kill(self, ctx: commands.Context):
        """Admin Only: yb.kill, kills the current yb bot process"""
        if not await self.bot.loop.create_task(self.checkadministrator(ctx)):
            return

        if ctx.message.guild.voice_client:
            await ctx.message.guild.voice_client.disconnect()
        else:
            await ctx.message.channel.send(f"yb bot is not in a voice channel currently.")

        if ctx.message.guild.id in players:
            print('Killed!')
            ctx.message.guild.voice_client.stop()
            players[ctx.message.guild.id].queue._queue.clear()
            del players[ctx.message.guild.id]

        await ctx.message.channel.send(f"yb bot process successfully terminated!")

    @commands.command()
    async def lock(self, ctx: commands.Context):
        """Admin Only: yb.lock, locks yb bot functionality"""
        if not await self.bot.loop.create_task(self.checkadministrator(ctx)):
            return

        if ctx.message.guild.id in players:
            if players[ctx.message.guild.id].locked:
                await ctx.message.channel.send(f"Already locked. Do yb.unlock to unlock the bot.")
                return
            else:
                players[ctx.message.guild.id].locked = True
                players[ctx.message.guild.id].lockrequester = ctx.message.author
        else:
            await ctx.message.channel.send(f"There are currently no yb bot player instances running in your server.")

        await ctx.message.channel.send(f"yb bot music functionality is currently locked by administrator {players[ctx.message.guild.id].lockrequester}! Ask an administrator to unlock the bot for your access.")

    @commands.command()
    async def unlock(self, ctx: commands.Context):
        """Admin Only: yb.unlock, unlocks yb bot functionality"""
        if not await self.bot.loop.create_task(self.checkadministrator(ctx)):
            return

        if ctx.message.guild.id in players:
            if not players[ctx.message.guild.id].locked:
                await ctx.message.channel.send(f"Already unlocked. Do yb.lock to lock the bot.")
                return
            else:
                players[ctx.message.guild.id].locked = False
                players[ctx.message.guild.id].lockrequester = ctx.message.author
        else:
            await ctx.message.channel.send(f"There are currently no yb bot player instances running in your server.")

        await ctx.message.channel.send(f"yb bot music functionality unlocked!")

        return

    @commands.command(aliases = ["stop", "ps"])
    async def pause(self, ctx: commands.Context):
        """yb.ps, pauses the song if currently playing"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if ctx.message.author.voice.channel == ctx.message.guild.voice_client.channel:
            if not players[ctx.message.guild.id].currentsource:
                await ctx.message.channel.send('yb bot is not currently playing anything!')
                return
            else:
                if ctx.message.guild.voice_client.is_paused():
                    await ctx.message.channel.send('Currently paused...')
                    return

                ctx.message.guild.voice_client.pause()
                await ctx.message.channel.send('Paused!')
        else:
            await ctx.message.channel.send('You must be in the voice channel with yb bot to do that!')
            return
    
    @commands.command(aliases = ["l", "lt"])
    async def loop(self, ctx: commands.Context):
        """yb.ps, pauses the song if currently playing"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if ctx.message.author.voice.channel == ctx.message.guild.voice_client.channel:
            if not players[ctx.message.guild.id].currentsource:
                await ctx.message.channel.send('yb bot is not currently playing anything!')
                return
            else:
                if players[ctx.message.guild.id].looptrack:
                    players[ctx.message.guild.id].looptrack = False
                    await ctx.message.channel.send('Unlooped track.')
                else:
                    players[ctx.message.guild.id].looptrack = True
                    await ctx.message.channel.send('Looping track.')
        else:
            await ctx.message.channel.send('You must be in the voice channel with yb bot to do that!')
            return

    @commands.command(aliases = ["resume", "res", "ups"])
    async def unpause(self, ctx: commands.Context):
        """yb.ups, unpauses the song if currently paused"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if ctx.message.author.voice.channel == ctx.message.guild.voice_client.channel:
            if not players[ctx.message.guild.id].currentsource:
                await ctx.message.channel.send('yb bot is not currently playing anything!')
                return
            else:
                if ctx.message.guild.voice_client.is_playing():
                    await ctx.message.channel.send('Currently playing...')
                    return

                ctx.message.guild.voice_client.resume()
                await ctx.message.channel.send('Resumed!')
        else:
            await ctx.message.channel.send('You must be in the voice channel with yb bot to do that!')
            return

    @commands.command(aliases = ["np", "playing"])
    async def nowplaying(self, ctx: commands.Context):
        """yb.np, displays the current song"""
        # Add artist names to this. Also log the current amount of listeners. Check if they have the bot muted and if they don't, count them as listener.
        # Rewrite this using the players nowplaying variable.
        # Allow server users to upvote and downvote songs.
        # Make sure users can't add more reactions to this message.
        if ctx.message.guild.id in players:
            if players[ctx.message.guild.id].currentsource:
                format = f'`{players[ctx.message.guild.id].currentsource.title}` by `{players[ctx.message.guild.id].currentsource.artist}` \nRequested by: 'f'`{players[ctx.message.guild.id].currentsource.requester}`'
                embed = discord.Embed(title=f'Now Playing:', description = format, colour = discord.Colour.random())
                embed.set_image(url = f'{players[ctx.message.guild.id].currentsource.artwork_url}')
                await ctx.message.channel.send(embed = embed)
            else:
                await ctx.message.channel.send('Nothing currently playing.')
                return
        else:
            await ctx.message.channel.send('Nothing currently playing.')
            return

    @commands.command(aliases = ["q", "qu"])
    async def queue(self, ctx: commands.Context):
        """yb.q, displays the current song queue"""
        # Add artist names to this. Also log the current amount of listeners. Check if they have the bot muted and if they don't, count them as listener.
        # Maybe also add album art to this.
        if ctx.guild.id in players:
            if players[ctx.guild.id].queue.empty():
                if players[ctx.guild.id].currentsource:
                    format = f'`{players[ctx.guild.id].currentsource.title}` by `{players[ctx.guild.id].currentsource.artist}` \nRequested by: 'f'`{players[ctx.guild.id].currentsource.requester}`\nCurrently no songs upcoming.'
                    embed = discord.Embed(title=f'Now Playing:', description = format, colour = discord.Colour.random())
                    await ctx.send(embed = embed)
                else:
                    await ctx.send('Nothing currently playing.')
                return
        else:
            await ctx.send('Nothing currently playing.')
            return

        upcoming = list(players[ctx.guild.id].queue._queue)
        chunks = [upcoming[x:x+10] for x in range(0, len(upcoming), 10)]

        currentchunk = 0
        format = ''

        tracknumber = currentchunk * 10

        format += f'**Now Playing:** `{players[ctx.guild.id].currentsource.title}` by `{players[ctx.guild.id].currentsource.artist}` \nRequested by: 'f'`{players[ctx.guild.id].currentsource.requester}`\n\n'
        for track in chunks[currentchunk]:
            format += f'{tracknumber + 1}\t**`{track["title"]}`**\n'
            tracknumber += 1
        embed = discord.Embed(title=f'{len(upcoming)} Songs In Queue : Page {1} ', description=format, colour = discord.Colour.random())

        message = await ctx.send(embed=embed)

        try:
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')
        except:
            await message.channel.send('yb Bot needs reaction add permissions to add pages to the queue message')

        def check(reaction, user):
            return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)

        while True:
            try:
                reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 300)
            except asyncio.TimeoutError:
                return

            if str(reaction.emoji) == "➡️":
                format = ''
                if currentchunk == len(chunks) - 1:
                    currentchunk = 0
                else:
                    currentchunk += 1
                tracknumber = currentchunk * 10
                
                format += f'**Now Playing:** `{players[ctx.guild.id].currentsource.title}` by `{players[ctx.guild.id].currentsource.artist}` \nRequested by: 'f'`{players[ctx.guild.id].currentsource.requester}`\n\n'
                for track in chunks[currentchunk]:
                    format += f'{tracknumber + 1}\t**`{track["title"]}`**\n'
                    tracknumber += 1
                embed = discord.Embed(title=f'{len(upcoming)} Songs In Queue : Page {currentchunk + 1} ', description=format, colour = discord.Colour.random())

                await message.edit(embed = embed)

            if str(reaction.emoji) == "⬅️":
                format = ''
                if currentchunk == 0:
                    currentchunk = len(chunks) - 1
                else:
                    currentchunk -= 1
                tracknumber = currentchunk * 10

                format += f'**Now Playing:** `{players[ctx.guild.id].currentsource.title}` by `{players[ctx.guild.id].currentsource.artist}` \nRequested by: 'f'`{players[ctx.guild.id].currentsource.requester}`\n\n'
                for track in chunks[currentchunk]:
                    format += f'{tracknumber + 1}\t**`{track["title"]}`**\n'
                    tracknumber += 1
                embed = discord.Embed(title=f'{len(upcoming)} Songs In Queue : Page {currentchunk + 1} ', description=format, colour = discord.Colour.random())

                await message.edit(embed = embed)
            
            await reaction.remove(author)

    @commands.command(aliases = ["h"])
    async def history(self, ctx: commands.Context, *, play: str = None):
        """Indev"""
        if play:
            split = play.split(' ')
            if split[0] == 'play':
                if split[1][0] == '-':
                    number = split[1][1:4]
                    if number.isdigit():
                        if str(ctx.message.guild.id) in previoushistory:
                            if not (int(number) > len(previoushistory[str(ctx.message.guild.id)])):
                                await ctx.send(f'```ini\n[Adding 1 song to the Queue.]\n```', delete_after = 15)
                                if not await self.bot.loop.create_task(self.connect(ctx)):
                                    return
                                if ctx.message.guild.id in players:
                                    await players[ctx.message.guild.id].queue.put(previoushistory[str(ctx.message.guild.id)][int(number) - 1])
                                    return
                                else:
                                    player = MusicPlayer(ctx)
                                    players[ctx.message.guild.id] = player
                                    await players[ctx.message.guild.id].queue.put(previoushistory[str(ctx.message.guild.id)][int(number) - 1])
                                    return

        if str(ctx.message.guild.id) in serverhistory:
            if not serverhistory[str(ctx.message.guild.id)]:
                await ctx.send('No history for the server.')
                return
        else:
            await ctx.send('No history for the server.')
            return

        upcoming = serverhistory[str(ctx.message.guild.id)]
        previoushistory[str(ctx.message.guild.id)] = upcoming
        chunks = [upcoming[x:x+10] for x in range(0, len(upcoming), 10)]

        currentchunk = 0
        format = ''

        tracknumber = currentchunk * 10

        for track in chunks[currentchunk]:
            format += f'-{tracknumber + 1}\t**`{track["title"]}`**\n'
            tracknumber += 1
        embed = discord.Embed(title=f'{len(upcoming)} In Server History : Page {currentchunk + 1} ', description=format, colour = discord.Colour.random())

        message = await ctx.send(embed=embed)

        try:
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')
        except:
            await message.channel.send('yb Bot needs reaction add permissions to add pages to the history message')

        def check(reaction, user):
            return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)

        while True:
            try:
                reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 300)
            except asyncio.TimeoutError:
                return

            if str(reaction.emoji) == "➡️":
                format = ''
                if currentchunk == len(chunks) - 1:
                    currentchunk = 0
                else:
                    currentchunk += 1
                tracknumber = currentchunk * 10
                
                for track in chunks[currentchunk]:
                    format += f'-{tracknumber + 1}\t**`{track["title"]}`**\n'
                    tracknumber += 1
                embed = discord.Embed(title=f'{len(upcoming)} In Server History : Page {currentchunk} ', description=format, colour = discord.Colour.random())

                await message.edit(embed = embed)

            if str(reaction.emoji) == "⬅️":
                format = ''
                if currentchunk == 0:
                    currentchunk = len(chunks) - 1
                else:
                    currentchunk -= 1
                tracknumber = currentchunk * 10

                for track in chunks[currentchunk]:
                    format += f'-{tracknumber + 1}\t**`{track["title"]}`**\n'
                    tracknumber += 1
                embed = discord.Embed(title=f'{len(upcoming)} In Server History : Page {currentchunk} ', description=format, colour = discord.Colour.random())

                await message.edit(embed = embed)
            
            await reaction.remove(author)

    @commands.command(aliases = ["uh"])
    async def userhistory(self, ctx: commands.Context, user: discord.Member = None):
        """Indev"""
        type = 'user'
        if not user:
            type = 'author'
            user = ctx.message.author

        if str(user.id) in userhistory:
            if not len(userhistory[str(user.id)]):
                await ctx.send(f'No history for the {type}.')
                return
        else:
            await ctx.send(f'No history for the {type}.')
            return

        upcoming = userhistory[str(user.id)]
        previoushistory[str(ctx.message.guild.id)] = upcoming
        chunks = [upcoming[x:x+10] for x in range(0, len(upcoming), 10)]

        currentchunk = 0
        format = ''

        tracknumber = currentchunk * 10

        for track in chunks[currentchunk]:
            format += f'-{tracknumber + 1}\t**`{track["title"]}`**\n'
            tracknumber += 1
        embed = discord.Embed(title=f'{len(upcoming)} In User History : Page {currentchunk + 1} ', description=format, colour = discord.Colour.random())

        message = await ctx.send(embed=embed)

        try:
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')
        except:
            await message.channel.send('yb Bot needs reaction add permissions to add pages to the history message')

        def check(reaction, user):
            return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)


        while True:
            try:
                reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 300)
            except asyncio.TimeoutError:
                return

            if str(reaction.emoji) == "➡️":
                format = ''
                if currentchunk == len(chunks) - 1:
                    currentchunk = 0
                else:
                    currentchunk += 1
                tracknumber = currentchunk * 10
                
                for track in chunks[currentchunk]:
                    format += f'-{tracknumber + 1}\t**`{track["title"]}`**\n'
                    tracknumber += 1
                embed = discord.Embed(title=f'{len(upcoming)} In User History : Page {currentchunk} ', description=format, colour = discord.Colour.random())

                await message.edit(embed = embed)

            if str(reaction.emoji) == "⬅️":
                format = ''
                if currentchunk == 0:
                    currentchunk = len(chunks) - 1
                else:
                    currentchunk -= 1
                tracknumber = currentchunk * 10

                for track in chunks[currentchunk]:
                    format += f'-{tracknumber + 1}\t**`{track["title"]}`**\n'
                    tracknumber += 1
                embed = discord.Embed(title=f'{len(upcoming)} In User History : Page {currentchunk} ', description=format, colour = discord.Colour.random())

                await message.edit(embed = embed)
            
            await reaction.remove(author)

    @commands.command(aliases = ["b"])
    async def back(self, ctx: commands.Context):
        """yb.b, add the previously played song to the front"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if not await self.bot.loop.create_task(self.connect(ctx)):
            return

        await players[ctx.message.guild.id].back()

        if not ctx.message.guild.voice_client.is_playing():
            if not ctx.message.guild.voice_client.is_paused():
                ctx.bot.loop.create_task(players[ctx.message.guild.id].audio_player())

        return

    @commands.command(aliases = ["lyr"])
    async def lyrics(self, ctx: commands.Context):
        """Indev"""
        guildid = ctx.message.guild.id
        artist = players[guildid].source['artist']
        track = players[guildid].source['title']

        try:
            if artist in track:
                result = genius.search(f'{track}')['hits'][0]['result']['id']
            else:
                result = genius.search(f'{artist} {track}')['hits'][0]['result']['id']
            lyrics = genius.lyrics(result)
            embed = discord.Embed(title = f'Lyrics for **{track}** by **{artist}**', description = f'{lyrics}')
        except:
            if artist in track:
                embed = discord.Embed(title = f'Couldn\'t find lyrics for **{track}**', description = f' ... ')
            else:
                embed = discord.Embed(title = f'Couldn\'t find lyrics for **{track}** by **{artist}**', description = f' ... ')
            
        
        await ctx.message.channel.send(embed = embed)
        return

    @commands.command(aliases = ["rem"])
    async def remove(self, ctx: commands.Context, position: int = None):
        """yb.rem <position in queue to remove>"""
        if not position:
            await ctx.send('Invalid syntax: Try yb.r <queue position to move to remove>')

        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if ctx.message.author.voice:
            vc = ctx.message.author.voice.channel
            if ctx.guild.voice_client:
                if not (vc == ctx.guild.voice_client.channel):
                    await ctx.send('You must be in the voice chat with yb bot...')
                    return
            else:
                await vc.connect()
        else:
            await ctx.send(f"You must join a voice channel to invite yb bot!")
            return
        
        # Not Tested
        if not ((position <= 0) or (position > len(players[ctx.guild.id].queue._queue))):
            await players[ctx.guild.id].remove(position - 1)

        await ctx.send(f"Operation successfully performed!")

        return

    @commands.command(aliases = ["shuf", "sh"])
    async def shuffle(self, ctx: commands.Context):
        """yb.sh, randomly sorts the queue"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if ctx.message.author.voice:
            vc = ctx.message.author.voice.channel
            if ctx.guild.voice_client:
                if not (vc == ctx.guild.voice_client.channel):
                    await ctx.send('You must be in the voice chat with yb bot...')
                    return
            else:
                await vc.connect()
        else:
            await ctx.send(f"You must join a voice channel to invite yb bot!")
            return
        
        await players[ctx.guild.id].shuffle()

        await ctx.send(f"Queue has been shuffled!")

        return

    @commands.command(aliases = ["movf", "mf", "movef", "front"])
    async def movefront(self, ctx: commands.Context, position: int = None):
        """yb.mf <queue position to move to front>"""
        if not position:
            await ctx.send('Invalid syntax: Try yb.mf <queue position to move to front>')

        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return

        if ctx.message.author.voice:
            vc = ctx.message.author.voice.channel
            if ctx.guild.voice_client:
                if not (vc == ctx.guild.voice_client.channel):
                    await ctx.send('You must be in the voice chat with yb bot...')
                    return
            else:
                await vc.connect()
        else:
            await ctx.send('You must join a voice channel to invite yb bot!')
            return
        
        if not ((position <= 0) or (position > len(players[ctx.guild.id].queue._queue))):
            await players[ctx.guild.id].move_front(position - 1)

        await ctx.send('Operation successfully performed!')

        return

    @commands.command(aliases = ['s'])
    async def skip(self, ctx: commands.Context, position: int = 1):
        """yb.s <Optional: position in queue to skip to>"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return

        if position:
            if not ctx.message.author.guild_permissions.administrator:
                if not await self.bot.loop.create_task(self.checkdj(ctx)):
                    return

        if not ctx.guild.voice_client.is_playing():
            return await ctx.send('Not playing any music right now...')
        
        clear = position > len(list(players[ctx.guild.id].queue._queue))

        if ctx.guild.voice_client.is_playing:
            ctx.guild.voice_client.stop()
            if clear:
                players[ctx.guild.id].queue._queue.clear()
            else:
                await players[ctx.guild.id].skip(position - 1)

    @commands.command(aliases = ['cl', 'c', 'clr'])
    async def clear(self, ctx: commands.Context):
        """yb.s <Optional: position in queue to skip to>"""
        if not ctx.message.author.guild_permissions.administrator:
            if await self.bot.loop.create_task(self.checklocked(ctx)):
                return
            if not await self.bot.loop.create_task(self.checkdj(ctx)):
                return
        
        if ctx.guild.voice_client.is_playing:
            players[ctx.guild.id].queue._queue.clear()

class ServerBuilding(commands.Cog):
    def __init__(self, yb):
        self.bot = yb
        
    @commands.command(aliases=["color", "cg"])
    async def colorgenerate(self, ctx, i, j, k, l):
        """Example: yb.colorgenerate db42a0 7a0000 01 10"""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Insufficient permissions...')
            return

        guild = ctx.guild
        await ctx.send('Generating color role gradient...')

        currentrole = int(k)
        temp = []

        iter = (int(l) - int(k))
        hex1 = int(i, 16)
        hex2 = int(j, 16)
        rgb1 = [ (hex1 & 0xFF0000) >> 16 , (hex1 & 0x00FF00) >> 8 , hex1 & 0x0000FF ]
        rgb2 = [ (hex2 & 0xFF0000) >> 16 , (hex2 & 0x00FF00) >> 8 , hex2 & 0x0000FF ]

        ranges = [ rgb1[0] - rgb2[0] , rgb1[1] - rgb2[1] , rgb1[2] - rgb2[2] ]
        iteration = [ ranges[0] / iter , ranges[1] / iter , ranges[2] / iter ]
        
        for x in range(iter + 1):
            role_name = f'{currentrole:02}'
           
            
            role = await guild.create_role( name = role_name , color = discord.Colour.from_rgb( math.floor(float(rgb1[0]) - (iteration[0] * x)) ,  math.floor(float(rgb1[1]) - (iteration[1] * x)) , math.floor(float(rgb1[2]) - (iteration[2] * x)) ) )
            temp.append(role.id)
            currentrole += 1

        await ctx.send('Color role gradient has been created!')
        

        if str(ctx.message.guild.id) in rolescreated:
            rolescreated[str(ctx.message.guild.id)].append(temp)
        else:
            rolescreated[str(ctx.message.guild.id)] = [temp]

        if str(ctx.message.guild.id) in undoroster:
            undoroster[str(ctx.message.guild.id)].append("rolescreate")
        else:
            undoroster[str(ctx.message.guild.id)] = ["rolescreate"]

    @commands.command(aliases = ["u"])
    async def undo(self, ctx: commands.Context, iterations = 1):
        """Example: yb.undo 2 (Undoes last two commands, default is one.)"""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Insufficient permissions...')
            return

        if str(ctx.message.guild.id) in undoroster:
            if not len(undoroster[str(ctx.message.guild.id)]):
                await ctx.send("Nothing to be undone!")
                return
            maxindex = iterations - 1
            format = ''
            for i in range(maxindex + 1):
                format += f'{i + 1} {undoroster[str(ctx.message.guild.id)][i]}\n'

            embed = discord.Embed(title=f'Undo Roster:', description = format, colour = discord.Colour.random())
            message = await ctx.send(embed = embed)

            await message.add_reaction('❌')
            await message.add_reaction('✅')

            check = lambda r, u: u == ctx.author and str(r.emoji) in "❌✅"

            switch = True

            while switch:
                try:
                    reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 100)
                except asyncio.TimeoutError:
                    return
                    
                if str(reaction.emoji) == "❌":
                    await reaction.remove(author)
                    return
                elif str(reaction.emoji) == "✅":
                    switch = False
                    await reaction.remove(author)

            for x in range(iterations):
                if len(undoroster[str(ctx.message.guild.id)]):
                    if undoroster[str(ctx.message.guild.id)][-1] == "rolescreate":
                        for i in rolescreated[str(ctx.message.guild.id)][-1]:
                            role = discord.utils.get(ctx.message.guild.roles, id = i )
                            if role:
                                await role.delete()
                                await ctx.send("The role {} has been deleted!".format(role.name))
                            else:
                                await ctx.send("The role doesn't exist!")
                        rolescreated[str(ctx.message.guild.id)].pop()
                    elif undoroster[str(ctx.message.guild.id)][-1] == "rolesdelete":
                        for i in rolesdeleted[str(ctx.message.guild.id)][-1]:
                            await ctx.guild.create_role(name = i['name'], color = i['color'], permissions = i['permissions'], hoist = i['hoist'], mentionable = i['mentionable'])

                            await ctx.send("The role {} has been created!".format(i.name))
                        await ctx.send("Be sure to move the roles back to where they were, you can use yb.moveroles <role_to_move_above> <roles_to_move_list> for that, and add back members.")
                        rolesdeleted[str(ctx.message.guild.id)].pop()
                else:
                    await ctx.send("Nothing to be undone!")
                    return
                await ctx.send(f"Undid {undoroster[str(ctx.message.guild.id)][-1]}!")
                undoroster[str(ctx.message.guild.id)].pop()
        else:
            await ctx.send("Nothing to be undone!")
        return

    @commands.command(aliases = ["del","delroles","delete","delrole","deleterole"])
    async def deleteroles(self, ctx: commands.Context, *, roles: str):
        """Example: yb.deleteroles 01 02 03 04 05 06..."""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Insufficient permissions...')
            return

        temp = []

        split = roles.split(' ')
        for i in split:
            role = discord.utils.get(ctx.message.guild.roles, name = i)
            if role:
                temp.append({'name': role.name, 'color': role.color, 'permissions': role.permissions, 'mentionable': role.mentionable, 'hoist': role.hoist})
                await role.delete()
                await ctx.send("The role {} has been deleted!".format(role.name))
            else:
                await ctx.send("The role doesn't exist!")

        if str(ctx.message.guild.id) in rolesdeleted:
            rolesdeleted[str(ctx.message.guild.id)].append(temp)
        else:
            rolesdeleted[str(ctx.message.guild.id)] = [temp]

        if str(ctx.message.guild.id) in undoroster:
            undoroster[str(ctx.message.guild.id)].append("rolesdelete")
        else:
            undoroster[str(ctx.message.guild.id)] = ["rolesdelete"]

    @commands.command(aliases = ["emoji","emote", "roleemote", "coloremote"])
    async def generateroleemote(self, ctx: commands.Context, shape: str, *, roles: str):
        """Example: yb.generateroleemote circle 01 02 03 04 05 06..."""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Insufficient permissions...')
            return

        if (shape == "heart") | (shape == 'Heart'):
            im = Image.open('heart.png')
        elif (shape == 'circle') | (shape == 'Circle'):
            im = Image.open('circle.png')
        else:
            await ctx.send("Invalid shape! Currently supported shapes are circle, heart. Suggest more shapes to Digital Artifact#5352.")
            return

        split = roles.split(' ')

        os.mkdir(f'{ctx.guild.id}')
    
        for i in split:
            temp = im.convert('RGBA')
            data = np.array(temp)
            r, g, b, a = data.T

            role = discord.utils.get(ctx.message.guild.roles, name = i)
            if role:
                color = role.color.to_rgb()
                white = (r == 255) & (b == 255) & (g == 255)
                data[..., :-1][white.T] = color
                final = Image.fromarray(data)
                await ctx.send(f'Creating emote for role {i}\'s color!')

                final.save(f'{ctx.guild.id}/{i}.png')
            else:
                await ctx.send("The role doesn't exist!")

        await ctx.send("Emotes successfully generated! Custom zip below created for your guild!")

        shutil.make_archive(f'{ctx.guild.id}', 'zip', f'{ctx.guild.id}')
        await ctx.send(file=discord.File(f'{ctx.guild.id}.zip'))
        os.remove(f'{ctx.guild.id}.zip')
        shutil.rmtree(f'{ctx.guild.id}')

    @commands.command(aliases = ["moverole"])
    async def moveroles(self, ctx: commands.Context, anchor: str, *, roles: str):
        """Example: yb.generateroleemote metaspacentity 01 02 03 04 (Role to move above and role list.)"""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Insufficient permissions...')
            return

        split = roles.split(' ')

        center = discord.utils.get(ctx.message.guild.roles, name = anchor)
        if center:
            for i in split:
                center = discord.utils.get(ctx.message.guild.roles, name = anchor)
                role = discord.utils.get(ctx.message.guild.roles, name = i)
                
                if role:
                    await role.edit(reason = None, position = center.position)
                else:
                    await ctx.send("The role doesn't exist!")

            await ctx.send("Roles successfully moved!")
        else:
            await ctx.send("The role doesn't exist!")

    @commands.command(aliases = ["renamerole"])
    async def renameroles(self, ctx: commands.Context, anchor: str, *, roles: str):
        """Indev"""

class Utility(commands.Cog):
    def __init__(self, yb):
        self.bot = yb

    @commands.command()
    async def purge(self, ctx: commands.Context):
        try:
            if ctx.message.author.guild_permissions.administrator:
                for i in messagehistory[str(ctx.message.guild.id)][str(ctx.message.channel.id)]:
                    await i.data.delete()
                messagehistory[str(ctx.message.guild.id)][str(ctx.message.channel.id)].clear()
            else:
                await ctx.send('You need admin for that...')
        except:
            await ctx.send('Something went wrong...')
        return

    @commands.command()
    async def kick(self, ctx: commands.Context, *, target: discord.User, reason: str):
        try:
            if ctx.message.author.guild_permissions.administrator:
                await ctx.guild.kick(user = target, reason = reason)
                if not ctx.guild.get_member(user_id=target.id).guild_permissions.administrator:
                    await ctx.send(f'Kicked user {target} for reason: {reason}')
                else:
                    await ctx.send('That person is an admin, you can\'t do that...')
            else:
                await ctx.send('You need admin for that...')
        except:
            await ctx.send('Something went wrong, command syntax is yb.kick <user> <reason>...')
        return

    @commands.command()
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.message.guild

        embed = discord.Embed(title=f'discord.gg{guild.name}', color = discord.Color.random())
        embed.set_author(name="revive Bot", url=f'{guild.icon_url}', icon_url=f'{guild.icon_url}')
        embed.add_field(name="General Info:", value=f'⋆Owner: {guild.owner}\n⋆Total Members: {guild.member_count}\n⋆Created: {str(guild.created_at)}\n⋆ID: {guild.id}', inline=False)
        embed.add_field(name="Channels & Roles:", value=f'⋆Text Channels: {len(guild.text_channels)}\n⋆Voice Channels: {len(guild.voice_channels)}\n⋆Categories: {len(guild.categories)}\n⋆Roles: {len(guild.roles)}', inline=False)
        embed.set_footer(text = f'discord.gg{guild.name}', icon_url = f'{guild.icon_url}')
        embed.set_image(url = f'{guild.banner_url}')
        embed.set_thumbnail(url = f'{guild.icon_url}')

        await ctx.send(embed = embed)
        return

    @commands.command()
    async def ban(self, ctx: commands.Context, target: discord.User, *, reason: str):
        try:
            if ctx.message.author.guild_permissions.administrator:
                await ctx.guild.ban(user = target, reason = reason)
                if not ctx.guild.get_member(user_id=target.id).guild_permissions.administrator:
                    await ctx.send(f'Banned user {target} for reason: {reason}')
                else:
                    await ctx.send('That person is an admin, you can\'t do that...')
            else:
                await ctx.send('You need admin for that...')
        except:
            await ctx.send('Something went wrong, command syntax is yb.ban <user> <reason>...')
        return

    @commands.command()
    async def prefix(self, ctx: commands.Context, *, prefixes: str):
        """<prefix_list>"""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Insufficient permissions...')
            return

        customprefixes[str(ctx.message.guild.id)] = prefixes.split() or defaultprefixes
        await ctx.send("Prefixes set!")

    @commands.command(aliases = ["av"])
    async def avatar(self, ctx: commands.Context, user: discord.Member = None):
        if not user:
            embed = discord.Embed(title = f'{ctx.message.author}', colour = discord.Colour.random()) 
            embed.set_image(url = str(ctx.message.author.avatar_url))
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = f'{user}', colour = discord.Colour.random())
            embed.set_image(url = user.avatar_url)
            await ctx.send(embed = embed)
        return

    @commands.command()
    async def banner(self, ctx: commands.Context, user: discord.Member = None):
        if user == None:
            req = await yb.http.request(discord.http.Route("GET", "/users/{uid}", uid = ctx.message.author.id))
            bannerid = req["banner"]
            if bannerid:
                type = requests.head(f"https://cdn.discordapp.com/banners/{ctx.message.author.id}/{bannerid}?size=1024").headers['Content-Type']
                if type == "image/gif":
                    bannerurl = f"https://cdn.discordapp.com/banners/{ctx.message.author.id}/{bannerid}.gif?size=1024"
                else:
                    bannerurl = f"https://cdn.discordapp.com/banners/{ctx.message.author.id}/{bannerid}?size=1024"
                embed = discord.Embed(title = f'{ctx.message.author}', colour = discord.Colour.random())
                embed.set_image(url = bannerurl)
                await ctx.send(embed = embed)
            else:
                return
        else:
                req = await yb.http.request(discord.http.Route("GET", "/users/{uid}", uid = user.id))
                bannerid = req["banner"]
                if bannerid:
                    type = requests.head(f"https://cdn.discordapp.com/banners/{user.id}/{bannerid}?size=1024").headers['Content-Type']
                    if type == "image/gif":
                        bannerurl = f"https://cdn.discordapp.com/banners/{user.id}/{bannerid}.gif?size=1024"
                    else:
                        bannerurl = f"https://cdn.discordapp.com/banners/{user.id}/{bannerid}?size=1024"
                    embed = discord.Embed(title = f'{user}', colour = discord.Colour.random())
                    embed.set_image(url = bannerurl)
                    await ctx.send(embed = embed)
                else:
                    return
        return

    @commands.command()
    async def help(self, ctx):
        currentchunk = 0
        message = await ctx.send(embed = helppages[currentchunk])

        try:
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')
        except:
            await message.channel.send('yb Bot needs reaction add permissions to add pages to the help message')

        def check(reaction, user):
            return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)

        while True:
            try:
                reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 300)
            except asyncio.TimeoutError:
                return
                
            if str(reaction.emoji) == "➡️":
                if currentchunk == len(helppages) - 1:
                    currentchunk = 0
                else:
                    currentchunk += 1

                await message.edit(embed = helppages[currentchunk])

                await reaction.remove(author)

            if str(reaction.emoji) == "⬅️":
                if currentchunk == 0:
                    currentchunk = len(helppages) - 1
                else:
                    currentchunk -= 1

                await message.edit(embed = helppages[currentchunk])
            
                await reaction.remove(author)

class Snipe(commands.Cog):
    def __init__(self, yb):
        self.bot = yb

    @commands.command()
    async def snipe(self, ctx):
            maxindex = len(lastonehundredmessages[str(ctx.message.guild.id)]) - 1
            format = ''
            ticker = 0
            chunks = []
            for i in range(maxindex + 1):
                format += f'{i + 1} {lastonehundredmessages[str(ctx.message.guild.id)][i]}\n'
                ticker += 1
                if ticker == 10:
                    chunks.append(format)
                    ticker = 0
                    format = ''

            if not (ticker == 0):
                chunks.append(format)

            currentchunk = 0

            embed = discord.Embed(title=f'Deleted Messages Page {currentchunk + 1}:', description = chunks[currentchunk], colour = discord.Colour.random())
            message = await ctx.send(embed = embed)

            try:
                await message.add_reaction('⬅️')
                await message.add_reaction('➡️')
            except:
                await message.channel.send('yb Bot needs reaction add permissions to add pages to the snipe message')

            def check(reaction, user):
                return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)

            while True:
                try:
                    reaction, author = await self.bot.wait_for("reaction_add", check = check, timeout = 300)
                except asyncio.TimeoutError:
                    return

                if str(reaction.emoji) == "➡️":
                    format = ''
                    if currentchunk == len(chunks) - 1:
                        await reaction.remove(author)
                        continue
                    currentchunk += 1
                    
                    embed = discord.Embed(title=f'Deleted Messages Page {currentchunk + 1}:', description = chunks[currentchunk], colour = discord.Colour.random())
                    await message.edit(embed = embed)

                if str(reaction.emoji) == "⬅️":
                    format = ''
                    if currentchunk == 0:
                        await reaction.remove(author)
                        continue
                    currentchunk -= 1
                    
                    embed = discord.Embed(title=f'Deleted Messages Page {currentchunk + 1}:', description = chunks[currentchunk], colour = discord.Colour.random())
                    await message.edit(embed = embed)
                
                await reaction.remove(author)

class Fun(commands.Cog):
    @commands.command(aliases = ["tc", "text"])
    async def textcomplete(self, ctx: commands.Context, *, prompt: str):
        """<prompt>"""
        await ctx.send('Please wait a few moments...')
        data = requests.post('https://api.inferkit.com/v1/models/standard/generate', 
                                json = {
                                        'prompt':{
                                            'text': prompt
                                            }, 
                                            'length': 500 
                                        }, 
                                headers = { 
                                        'Authorization': f'Bearer {inferkitbearerid}' 
                                        }
                                )
        embed =  discord.Embed(title = 'Powered by Inferkit API.', description = prompt + ' ' + data.json()['data']['text'])
        await ctx.send(embed = embed)

    @commands.command()
    async def cat(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def compatability(self, ctx: commands.Context, user: str):
        await ctx.send('Please wait a few moments, doing some very hard calculations...')
        author = ctx.message.author.id
        try:
            target = ctx.message.guild.get_member(user)
        except:
            await ctx.send("Invalid user!")
            return
        return

    @commands.command()
    async def catvideo(self, ctx: commands.Context):
        """Indev"""
        return
    
    @commands.command()
    async def dog(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def dogvideo(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def spirograph(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def googlesearch(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def aipainting(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def airpg(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def aimusicmaker(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def aisongimage(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def aivideo(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def dracomalfoy(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def aichatbot(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def fractal(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def mathtest(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def liedetector(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def bully(self, ctx: commands.Context):
        """Indev"""
        return

    @commands.command()
    async def aiplanet(self, ctx: commands.Context):
        """Indev"""
        return

async def determine_prefix(yb: Bot, message: discord.Message):
    if message.guild:
        return customprefixes.get(str(message.guild.id), defaultprefixes)
    else:
        return defaultprefixes

intents = discord.Intents.default()
intents.members = True
yb = commands.Bot(description='yb Bot', command_prefix = determine_prefix, intents = intents, help_command = None)

yb.add_cog(ServerBuilding(yb))
yb.add_cog(Utility(yb))
yb.add_cog(Fun())
yb.add_cog(Snipe(yb))
yb.add_cog(Music(yb))

@yb.event
async def on_ready():
    print('Discord version: ' + discord.__version__)
    print('We have logged in as {0.user}'.format(yb))
    await yb.change_presence(activity=discord.Game(name=f"r!help"))

@yb.event
async def on_message_delete(message):
    if str(message.guild.id) in lastonehundredmessages:
        lastonehundredmessages[str(message.guild.id)].insert(0, f'`{message.content}` sent by `{message.author}`\n')
        while len(lastonehundredmessages[str(message.guild.id)]) >= 101:
            lastonehundredmessages[str(message.guild.id)].pop()
    else:
        lastonehundredmessages[str(message.guild.id)] = [f'`{message.content}` sent by `{message.author}`\n']

@yb.event
async def on_bulk_message_delete(messages):
    for message in messages:
        if str(message.guild.id) in lastonehundredmessages:
            lastonehundredmessages[str(message.guild.id)].insert(0, f'`{message.content}` sent by `{message.author}`\n')
            while len(lastonehundredmessages[str(message.guild.id)]) >= 101:
                lastonehundredmessages[str(message.guild.id)].pop()
        else:
            lastonehundredmessages[str(message.guild.id)] = [f'`{message.content}` sent by `{message.author}`\n']

@yb.event
async def on_message(message):
    if str(message.guild.id) in messagehistory:
        if str(message.channel.id) in messagehistory[str(message.guild.id)]:
            messagehistory[str(message.guild.id)][str(message.channel.id)].insert(0, Message(snipe = f'`{message.content}` sent by `{message.author} in #{message.channel}`\n', data = message))
            while len(messagehistory[str(message.guild.id)][str(message.channel.id)]) >= 101:
                messagehistory[str(message.guild.id)][str(message.channel.id)].pop()
        else:
            messagehistory[str(message.guild.id)][str(message.channel.id)] = [Message(snipe = f'`{message.content}` sent by `{message.author} in #{message.channel}`\n', data = message)]
    else:
        messagehistory[str(message.guild.id)][str(message.channel.id)] = [Message(snipe = f'`{message.content}` sent by `{message.author} in #{message.channel}`\n', data = message)]

    await yb.process_commands(message)

@yb.event
async def on_guild_join(guild):
    try:
        general = next((x for x in guild.text_channels if x.name == 'general'), None)
    except:
        return

    currentchunk = 0
    message = await general.send(embed = helppages[currentchunk])

    try:
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')
    except:
        await message.channel.send('yb Bot needs reaction add permissions to add pages to the help message')

    def check(reaction, user):
        return (not user == message.author) and (str(reaction.emoji) in "⬅️➡️") and (reaction.message.id == message.id)

    while True:
        try:
            reaction, author = await yb.wait_for("reaction_add", check = check, timeout = 300)
        except asyncio.TimeoutError:
            return

        if str(reaction.emoji) == "➡️":
            if currentchunk == len(helppages) - 1:
                currentchunk = 0
            else:
                currentchunk += 1

            await message.edit(embed = helppages[currentchunk])

        if str(reaction.emoji) == "⬅️":
            if currentchunk == 0:
                currentchunk = len(helppages) - 1
            else:
                currentchunk -= 1

            await message.edit(embed = helppages[currentchunk])
        
        await reaction.remove(author)

yb.run(discordbottoken)
