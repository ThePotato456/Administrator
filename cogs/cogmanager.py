"""
Author: eddy22
Altered By: ThePotato456
"""

import asyncio
import json
from multiprocessing.dummy import Manager
import discord
import utils
from utils import colors
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

        await utils.message_embed(ctx, 'Cog Manager', "Reloading...", colors.blue, cleanupTime=3)
        try:
            for cog in listdir(path.join(path.dirname(path.realpath(__file__)))):
                if cog.endswith(".py") == True:
                    if not self.check_cog(cog) in self.unloaded_cogs:
                        self.bot.reload_extension(f"cogs.{cog[:-3]}")
                    else:
                        self.unloaded_cogs.remove(self.check_cog(cog))
                        self.bot.reload_extension(f'cogs.{cog[:-3]}')
        except discord.ExtensionNotLoaded as nl:
            await utils.error_embed(ctx, f'The extension {cog} was not loaded:\n```\n{nl}\n```')
        except discord.ExtensionNotFound as nf:
            await utils.error_embed(ctx, f'The extension {cog} was not found:\n```\n{nf}\n```')
        except discord.NoEntryPointError as ne:
            await utils.error_embed(ctx, f'The extension {cog} was does not have a setup function!')
        except discord.ExtensionFailed as ef:
            await utils.error_embed(ctx, f'The extension {cog} or its setup function has failed:\n```\n{ef}\n```')
        except Exception as exc:
            await utils.error_embed(ctx, f"An unknown error has occurred: {exc}")
        else:
            await utils.message_embed(ctx, 'Cog Manager', 'All cogs have been reloaded.', colors.blue)

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
        await utils.message_embed(ctx, 'Loading Cog', f'Loading {cog}.....', cleanupTime=3)
        try:
            if self.check_cog(cog) in self.unloaded_cogs:
                self.unloaded_cogs.remove(self.check_cog(cog))
            self.bot.load_extension(self.check_cog(cog))
        except discord.ExtensionNotFound as nf:
            await utils.error_embed(ctx, f'The extension {cog} was not found:\n```\n{nf}\n```')
        except discord.ExtensionAlreadyLoaded as al:
            await utils.error_embed(ctx, f'The extension {cog} is already loaded:\n```\n{al}\n```')
        except discord.NoEntryPointError:
            await utils.error_embed(ctx, f'The extension {cog} was does not have a setup function!')
        except discord.ExtensionFailed as ef:
            await utils.error_embed(ctx, f'The extension {cog} or its setup function has failed:\n```\n{al}\n```')
        except Exception as exc:
            await utils.error_embed(ctx, f"An error has occurred: \n```\n{exc}\n```")
        else:
            await utils.message_embed(ctx, 'Cog Manager', f"{self.check_cog(cog)} has been loaded.", colors.blue)

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
        await utils.message_embed(ctx, 'Cog Manager', f'Unloading {cog}', colors.blue, cleanupTime=3)
        try:
            self.bot.unload_extension(self.check_cog(cog))
        except discord.ExtensionNotFound:
            await utils.error_embed(ctx, f'The extension {cog} is not found!')
        except discord.ExtensionNotLoaded:
            await utils.error_embed(ctx, f'The extension {cog} is not loaded!')
        else:
            await utils.message_embed(ctx, 'Cog Manager', f"{self.check_cog(cog)} has been unloaded.", colors.blue)

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
        await utils.message_embed(ctx, 'Cog Manager', "Reloading...", colors.blue, cleanupTime=3)
        try:
            self.bot.reload_extension(self.check_cog(cog))
        except Exception as exc:
            await utils.error_embed(ctx, f"An error has occurred: {exc}")
        else:
            await utils.message_embed(ctx, 'Cog Manager', f"{self.check_cog(cog)} has been reloaded.")
    
    @commands.command(name='listcogs', hidden=True)
    @commands.is_owner()
    async def list_cogs(self, ctx: commands.Context):
        await ctx.message.delete()
        loaded_cogs = list(self.bot.extensions.keys())
        await utils.message_embed(ctx, 'Loaded Cogs', (f'[!] Loaded Cogs: ```JSON\n{json.dumps(loaded_cogs)}\n```'
                      +f'[!] Unloaded Cogs: ```JSON\n{json.dumps(self.unloaded_cogs)}\n```'), colors.blue)

def setup(bot):
    """Every cog needs a setup function like this."""
    bot.add_cog(CogManager(bot))
