#256064
import discord
from discord import channel
from discord import client

from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

from discord.ext import commands
from datetime import date, datetime, timedelta


message_lastseen = datetime.now()

bot = commands.Bot(command_prefix="s!", help_command=None)

@bot.event
async def on_ready():
    print("logged in as {bot.user}")

@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="Spinebot Commands", description="คำสั่งทั้งหมด", color=0x5a49e3)
    emBed.add_field(name="s!help", value="คำสั่งที่สามารถใช้ได้", inline=False)
    emBed.add_field(name="s!hello", value="ทักทาย", inline=False)
    emBed.add_field(name="s!play", value="เล่นเพลง", inline=False)
    emBed.add_field(name="s!leave", value="หยุดเพลง", inline=False)
    emBed.set_thumbnail(url="https://cdn.discordapp.com/attachments/861386789952290826/902391108112363581/Spine-logos.jpeg")
    emBed.set_footer(text="SpineBot", icon_url="https://cdn.discordapp.com/attachments/861386789952290826/902391108112363581/Spine-logos.jpeg")
    await ctx.channel.send(embed=emBed)

@bot.event
async def on_message(message):
    global message_lastseen
    if message.content == "s!hello":
        print(message.channel)
        await message.channel.send("สวัสดี " + str(message.author.name))
    elif message.content == "s!logout":
        await message.channel.send("ลาก่อน")
        await bot.logout()
    await bot.process_commands(message)

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None:
        ctx.channel.send("Joined")
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)

    YDL_OPTIONS = {'format' : 'bestaudio' , 'noplaylist' : 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice_client.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice_client.is_playing()
    else:
        await ctx.channel.send("เพลงกำลังเล่นอยู่แล้วครับเพื่อน")
        return

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run('OTAyMjUxMTY0MDIyNzUxMzMz.YXbs4A.rDcYqbJJFfaGPCBvt83bLiaEAI8')