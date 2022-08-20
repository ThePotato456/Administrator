import discord
from discord.ext import commands
import os
import dotenv


if __name__ == "__main__":
    administrator = commands.Bot(command_prefix="-", intents = discord.Intents.all())

    @administrator.event
    async def on_ready():
        print('[bot] Logged in as {0} ({0.id})'.format(administrator.user))
        print('[bot] Interact with it using the prefix \'-\'')
        print('[bot] Invite to your server with this link: {0}'.format('https://discord.com/api/oauth2/authorize?client_id=972616556347527258&permissions=8&scope=bot'))

    for file in os.listdir('cogs'):
        if file.endswith(".py"):
            name = file[:-3]
            print(f"[init] Loading cogs.{name}")
            administrator.load_extension(f"cogs.{name}")
    dotenv.load_dotenv()
    administrator.run(os.getenv("DISCORD_TOKEN"))