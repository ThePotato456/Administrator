
import discord, asyncio
from discord.ext import commands
from enum import Enum
from bot import admin
import utils

class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5

class Messages:
    NO_PERMS = 'You do not have permission to run this command!'
    USR_NOT_FOUND = 'Unable to find a user by that ID/Name!'
    USR_NOT_SPECIFIED = 'No user was specified for command!'
    USR_ALRDY_MUTED = "This user is already muted!"
    USR_NOT_MUTED = "This user os not muted"

class Sinks(Enum):
    mp3 = discord.sinks.MP3Sink()
    wav = discord.sinks.WaveSink()
    pcm = discord.sinks.PCMSink()
    ogg = discord.sinks.OGGSink()
    mka = discord.sinks.MKASink()
    mkv = discord.sinks.MKVSink()
    mp4 = discord.sinks.MP4Sink()
    m4a = discord.sinks.M4ASink()

async def get_user(ctx: commands.Context, user_id: str=None):
    if not user_id is None and str.isdigit(user_id):
        user = await utils.get_user_by_id(ctx, user_id)
    elif not user_id is None:
        user = await utils.get_user_by_name(ctx, str(user_id))
    else:
        user = await utils.get_user_by_id(ctx, int(ctx.author.id))
    return user

async def get_user_by_id(ctx: commands.Context, id: int=None):
    guild: discord.Guild = ctx.guild
    if not id is None:
        member: discord.Member = guild.get_member(int(id))
        return member

async def get_user_by_name(ctx: commands.Context, name: str=None):
    guild: discord.Guild = ctx.guild
    if not name is None and not name == "":
        if '<@' in name:
            user_id = name.replace('<@', '').replace('>', '')
            if str.isdigit(user_id):
                user_id = int(user_id)
                member: discord.Member = guild.get_member(int(user_id))
                return member
        else:
            for member in ctx.guild.members:
                if member.name == name or member.display_name == name:
                    return member
            return None

async def decode_time(time: str=None):
    if time is None:
        time = 120
    else:
        if 'm' in time:
            time = int(time.replace('m', ''))
            time = (time * 60)
        elif 'h' in time:
            time = int(time.replace('h', ''))
            time = (time * 60) * 60
        elif 's' in time:
            time = int(time.replace('s', ''))
    return time

async def message_embed(ctx: commands.Context, title, description, color=colors.blurple, shouldCleanup=True, cleanupTime=10, create=False):
    embed = discord.Embed(title=title, description='{0}'.format(description), color=color)
    if create: return embed
    message = await ctx.send(embed=embed)
    if shouldCleanup:
        await asyncio.sleep(cleanupTime)
        await message.delete()

async def error_embed(ctx: commands.Context, error_message, create=False, shouldCleanup=True, cleanupTime=10):
    embed = discord.Embed(title='Error', description='{0}'.format(error_message), color=colors.red)
    if create: return embed
    message = await ctx.send(embed=embed)
    if shouldCleanup:
        await asyncio.sleep(cleanupTime)
        await message.delete()

async def is_admin(ctx: commands.Context, user: discord.Member):
    admin_roles = admin.get_config('administrator_roles')
    for role in user.roles:
        if not role.name == '@everyone':
            for role_ in admin_roles:
                if role.id == int(role_):
                    return True
    return False

class Time(commands.Converter):
    async def convert(self, ctx: commands.Context, time: str=None):
        str_time = time
        if time is None:
            time = 120
        else:
            if 'm' in time:
                time = int(time.replace('m', ''))
                time = (time * 60)
            elif 'h' in time:
                time = int(time.replace('h', ''))
                time = (time * 60) * 60
            elif 's' in time:
                time = int(time.replace('s', ''))
        return { 'time': time, 'str_time': str_time }

async def translate_time(time_str: str=None):
    if not time_str is None:
        if 'm' in time_str:
            time = int(time_str.replace('m', ''))
            time = (time * 60)
        elif 'h' in time_str:
            time = int(time_str.replace('h', ''))
            time = (time * 60) * 60
        elif 's' in time_str:
            time = int(time_str.replace('s', ''))
    
        return time
