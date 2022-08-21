from collections import UserDict
from imaplib import Commands
from pydoc import isdata
import discord
from discord.ext import commands
import asyncio, json, os
import utils
from utils import colors, is_admin


class CommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[commands] CommandsCog loaded and ready ')

    @commands.command(name='massmove')
    async def massmove(self, ctx: commands.Context, prev_id: int=None, next_id: int=None):
        if not prev_id == None and not next_id == None:
            if await utils.is_admin(ctx, ctx.author):
                prev_channel: discord.VoiceChannel = self.bot.get_channel(prev_id)
                next_channel: discord.VoiceChannel = self.bot.get_channel(next_id)
                if not prev_channel == None and not next_channel == None:
                    member_ids = list(prev_channel.voice_states.keys())
                    
                    if not len(member_ids) == 0:
                        message = await utils.message_embed(ctx, title='Administrator', description=f'**__Moving users from__**-- `{prev_channel.name} -> {next_channel.name}`', color=colors.blurple, shouldCleanup=False)
                        for id in member_ids:
                            member: discord.Member = await ctx.guild.fetch_member(id)
                            await member.move_to(next_channel)
                    else:
                        await utils.error_embed(ctx, f'No users in `{prev_channel.name}`')
                    await ctx.message.delete()
                else:
                    if prev_channel == None:
                        await utils.error_embed(ctx, 'First channel ID is not valid!')
                    if next_channel == None:
                        await utils.error_embed(ctx, 'Second channel ID is not valid!')
            else:
                await utils.error_embed(ctx, utils.Messages.NO_PERMS)

    @commands.command()
    async def timeout(self, ctx: commands.Context, member: str=None):
        if await utils.is_admin(ctx, ctx.author) or ctx.message.author.id == '194151340090327041':
            guild: discord.Guild = ctx.guild
            if not member is None:
                muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="FED")
                verified_role: discord.Role = discord.utils.get(ctx.guild.roles, name='Verified')

                member: discord.Member = await utils.get_user(ctx, member)
                if member is None:
                    return await utils.error_embed(ctx, utils.Messages.USR_NOT_FOUND)

                muted_role = discord.utils.get(guild.roles, name='FED')
                if muted_role in member.roles:
                    return await utils.error_embed(ctx, utils.Messages.USR_ALRDY_MUTED)
                
                await member.add_roles(muted_role)
                await member.remove_roles(verified_role)
                await utils.message_embed(ctx, title="Timed Out!", description="**{0}** was timed out by **{1}**!".format(member, ctx.message.author), color=colors.red, shouldCleanup=False)
        else:
            await utils.error_embed(ctx, utils.Messages.NO_PERMS)
    
    @commands.command()
    async def untimeout(self, ctx: commands.Context, member: str=None):
        if await utils.is_admin(ctx, ctx.author):
            member: discord.Member = await utils.get_user(ctx, member)
            muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name='FED')
            verified_role: discord.Role = discord.utils.get(ctx.guild.roles, name='Verified')

            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                await member.add_roles(verified_role)
                await utils.message_embed(ctx, title='Unmuted', description=f'**{member}** was unmuted by **{ctx.author}**!', color=colors.green, shouldCleanup=False)
            else:
                await utils.error_embed(ctx, utils.Messages.USR_NOT_MUTED, shouldCleanup=False)

    @commands.command(aliases=['w', 'user'])
    async def whois(self, ctx: commands.Context, user_id: str=None):
        if await utils.is_admin(ctx, ctx.author):
            guild: discord.Guild = ctx.guild
            user: discord.Member = await utils.get_user(ctx, user_id)

            if user is None:
                return await utils.error_embed(ctx, 'Unable to find user by that ID/Name!')
            
            user_roles = ''
            for role in user.roles:
                if not role.name == '@everyone':
                    user_roles = user_roles + f'<@&{role.id}>'
            
            if await utils.is_admin(ctx, user):
                is_admin = 'yes'
            else:
                is_admin = 'no'

            description = (f'**__Member Name:__** <@{user.id}>\n')  + (f'**__Member ID:__** {user.id}\n') + (f'**__Roles:__**{user_roles}\n') + (f'**__Is Admin:__** {is_admin}\n')
            await utils.message_embed(ctx, title='User Info', description=description, color=colors.blurple, shouldCleanup=False)
        else:
            await utils.error_embed(ctx, 'You do not have permission to run this command!')

def setup(bot: commands.Bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(CommandsCog(bot))