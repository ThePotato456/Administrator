"""
Author: eddy22
Altered By: ThePotato456
"""

import asyncio
import json
from multiprocessing.dummy import Manager
import discord
from discord.ext import commands
from sys import version_info as sysv
from os import listdir, path

class CogManager(commands.Cog):
    """This is a cog with owner-only commands.
        Note:
                All cogs inherits from `commands.Cog`_.
                All cogs are classes, so they need self as first argument in their methods.
                All cogs use different decorators for commands and events (see example below).
                All cogs needs a setup function (see below).
    Documentation:
        https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.unloaded_cogs = []

    # This is the decorator for events (inside of cogs).
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[manager] Eddie's cog managaer loading.... Python {sysv.major}.{sysv.minor}.{sysv.micro} - py-cord {discord.__version__}")
        # Prints on the shell the version of Python and Discord.py installed in our computer.

    
    # This command is hidden from the help menu.
    # This is the decorator for commands (inside of cogs).
    # Only the owner (or owners) can use the commands decorated with this.
    @commands.command(name="reloadall", hidden=True)
    @commands.is_owner()
    async def reload_all(self, ctx):
        """This commands reloads all the cogs in the `./cogs` folder.

        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds."""

        message = await ctx.send("Reloading...")

        try:
            for cog in listdir(path.join(path.dirname(path.realpath(__file__)))):
                if cog.endswith(".py") == True:
                    if not self.check_cog(cog) in self.unloaded_cogs:
                        self.bot.reload_extension(f"cogs.{cog[:-3]}")
                    else:
                        self.unloaded_cogs.remove(self.check_cog(cog))
                        self.bot.reload_extension(f'cogs.{cog[:-3]}')
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content="All cogs have been reloaded.")
        await asyncio.sleep(3)
        await message.delete()
        await ctx.message.delete()

    def check_cog(self, cog):
        """Returns the name of the cog in the correct format.
        Args:
                self
                cog (str): The cogname to check
        Returns:
                cog if cog starts with `cogs.`, otherwise an fstring with this format`cogs.{cog}`_.
        Note:
                All cognames are made lowercase with `.lower()`_.
        """
        if (cog.lower()).startswith("cogs.") == True:
            return cog.lower()
        return f"cogs.{cog.lower()}"

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """This commands loads the selected cog, as long as that cog is in the `./cogs` folder.
        Args:
                cog (str): The name of the cog to load. The name is checked with `.check_cog(cog)`_.
        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds.
        """
        message = await ctx.send("Loading...")
        await ctx.message.delete()
        try:
            if self.check_cog(cog) in self.unloaded_cogs:
                self.unloaded_cogs.remove(self.check_cog(cog))
            self.bot.load_extension(self.check_cog(cog))
            

        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content=f"{self.check_cog(cog)} has been loaded.")
        await asyncio.sleep(3)
        await message.delete()

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """This commands unloads the selected cog, as long as that cog is in the `./cogs` folder.

        Args:
                cog (str): The name of the cog to unload. The name is checked with `.check_cog(cog)`_.
        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds.
        """
        message = await ctx.send("Unloading...")
        await ctx.message.delete()
        try:
            if self.check_cog(cog) not in self.unloaded_cogs:
                self.unloaded_cogs.append(self.check_cog(cog))
                self.bot.unload_extension(self.check_cog(cog))
            else:
                await message.edit(content='[!] Unloaded COG not found in list!')
                await message.edit(content='[*]Unloaded COGS:\n'
                                         + '```JSON\n'
                                         + f'{json.dumps(self.unloaded_cogs, indent=2)}'
                                         + '```')
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content=f"{self.check_cog(cog)} has been unloaded.")
        await asyncio.sleep(3)
        await message.delete()

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """This commands reloads the selected cog, as long as that cog is in the `./cogs` folder.
        Args:
                cog (str): The name of the cog to reload. The name is checked with `.check_cog(cog)`_.
        Note:
                This command can be used only from the bot owner.
                This command is hidden from the help menu.
                This command deletes its messages after 20 seconds.
        """
        message = await ctx.send("Reloading...")
        await ctx.message.delete()
        try:
            self.bot.reload_extension(self.check_cog(cog))
        except Exception as exc:
            await message.edit(content=f"An error has occurred: {exc}")
        else:
            await message.edit(content=f"{self.check_cog(cog)} has been reloaded.")
        await asyncio.sleep(3)
        await message.delete()
    
    @commands.command(name='listcogs', hidden=True)
    @commands.is_owner()
    async def list_cogs(self, ctx: commands.Context):
        await ctx.message.delete()
        loaded_cogs = list(self.bot.extensions.keys())
        message = await ctx.send(f'[!] Loaded COGS: ```JSON\n{json.dumps(loaded_cogs)}\n```'
                                +f'[!] Unloaded COGS: ```JSON\n{json.dumps(self.unloaded_cogs)}\n```')
        await asyncio.sleep(10)
        await message.delete()

def setup(bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(CogManager(bot))
