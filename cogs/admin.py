
from distutils.log import error
import discord
from discord.ext import commands
import asyncio, json, os
import utils
from utils import colors, is_admin

    # TODO: [✗] add ability to target channel when not in the voice call
    # TODO: [✗] add various different sound files
                                                                                                                                                                                                                                                                                                                                            # TODO: [✗] user muted
    # TODO: [✗] kick
    # TODO: [✓] whois
    # TODO: [✓] timeouwno``
class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[commands] loaded and ready ')

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
    async def ban(self, ctx: commands.Context, user: int=None, reason: str=None):
        if not user is None and not reason is None:
            target_user: discord.Member(utils.get_user(ctx, user))
            guild: discord.Guild  = ctx.author.guild
            guild.ban(user=target_user, reason=f'{reason}', )

    @commands.command()
    async def unban(self, ctx: commands.Context, user: str=None):
        guild: discord.Guild = ctx.guild
        if ctx.author.roles in guild.roles:
            return await utils.message_embed(ctx, title='', description='', color=colors.green)

            
    @commands.command()
    async def timeout(self, ctx: commands.Context, member: discord.Member=None, time: utils.Time=None):
        guild: discord.Guild = ctx.guild
        if not member is None:
            muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name="FED")
            verified_role: discord.Role = discord.utils.get(ctx.guild.roles, name='Verified')
            if member is None:
                return await utils.error_embed(ctx, utils.Messages.USR_NOT_FOUND)
            muted_role = discord.utils.get(guild.roles, name='FED')
            if muted_role in member.roles:
                return await utils.error_embed(ctx, utils.Messages.USR_ALRDY_MUTED)
            str_time = time['str_time']
            time = time['time']
            await member.add_roles(muted_role)
            await member.remove_roles(verified_role)
            await utils.message_embed(ctx, title="Timed Out!", description="**{0}** was timed out by **{1}** for {2}!".format(member, ctx.message.author, str_time), color=colors.red, shouldCleanup=False)
            if time != 0:
                while True:
                    time = time - 1
                    if time == 0:
                        break
                    await asyncio.sleep(1) 
            if muted_role in member.roles and not verified_role in member.roles:
                await self.untimeout(ctx, member.name)
            else:
                await utils.error_embed(ctx, f'{member.name} is not timed out!')
    
    @commands.command()
    async def untimeout(self, ctx: commands.Context, member: discord.Member=None):
        if await utils.is_admin(ctx, ctx.author):
            if member is None: return await utils.error_embed(ctx, error_message=utils.Messages.USR_NOT_SPECIFIED, shouldCleanup=False)
            muted_role: discord.Role = discord.utils.get(ctx.guild.roles, name='FED')
            verified_role: discord.Role = discord.utils.get(ctx.guild.roles, name='Verified')

            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                await member.add_roles(verified_role)
                await utils.message_embed(ctx, title='Untimeout', description=f'**{member}** was untimed out by **{ctx.author}**!', color=colors.green, shouldCleanup=False)
            else:
                await utils.error_embed(ctx, utils.Messages.USR_NOT_MUTED, shouldCleanup=False)

    @commands.command(aliases=['w', 'user'])
    async def whois(self, ctx: commands.Context, member: discord.Member=None):
        if await utils.is_admin(ctx, ctx.author):
            if member is None:
                member: discord.Member = ctx.author
                #return await utils.error_embed(ctx, 'Unable to find user by that ID/Name!')
            
            user_roles = ''
            for role in member.roles:
                if not role.name == '@everyone':
                    user_roles = user_roles + f'<@&{role.id}>'
            
            if await utils.is_admin(ctx, member):
                is_admin = 'yes'
            else:
                is_admin = 'no'

            description = (f'**__Member Name:__** <@{member.id}>\n')  + (f'**__Member ID:__** {member.id}\n') + (f'**__Roles:__**{user_roles}\n') + (f'**__Is Admin:__** {is_admin}\n')
            await utils.message_embed(ctx, title='User Info', description=description, color=colors.blurple, shouldCleanup=False)
        else:
            await utils.error_embed(ctx, 'You do not have permission to run this command!')

    @commands.command()
    async def nocam(self, ctx: commands.Context, member: discord.Member=None):
        if await utils.is_admin(ctx, ctx.author):
            if member is None: return await utils.error_embed(ctx, error_message=utils.Messages.USR_NOT_SPECIFIED, shouldCleanup=False)
            no_cam_role: discord.Role = discord.utils.get(ctx.guild.roles, name="Camera Disabled")
            original_channel: discord.VoiceChannel = member.voice.channel
            
            afk_channel: discord.VoiceChannel = self.bot.get_channel(1001109930289414164)

            if not no_cam_role in member.roles:
                await member.add_roles(no_cam_role)
                await utils.message_embed(ctx, title='No Camera Role', description=f'**{member}** was given the no camera role by **{ctx.author}**!', color=colors.green, shouldCleanup=False)
            else:
                await member.remove_roles(no_cam_role)
                await utils.message_embed(ctx, title='No Camera Role', description=f'The `Camera Disabled` role was removed **{member}** by **{ctx.author}**', color=colors.red, shouldCleanup=False)
            await member.move_to(afk_channel)
            await asyncio.sleep(0.05)
            await member.move_to(original_channel)


def setup(bot: commands.Bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(Admin(bot))