import discord
from discord.ext import commands
import os
import dotenv
import json
import utils

def load_config():
    if not os.path.exists('data/config.json'):
        open('./data/config.json', 'x+').write('{\n    "command_prefix": "",\n    "administrator_roles": [""]\n}')
    return json.load(open('./data/config.json', 'r'))
config = load_config()

class Administrator(commands.Bot):
    def __init__(self):
        self.config = load_config()
        self.bot = commands.Bot(command_prefix=self.config['command_prefix'], intents=discord.Intents.all())

    def get_config(self, key):
        if not self.config is None:
            return self.config[key]

    @commands.command(name='reload-config')
    async def reload_config(self, ctx: commands.Context):
        self.config = self.load_config()
        await utils.message_embed(ctx, title='Administrator', description=f'**__Reloading config...__**', color=utils.colors.blue)
    
admin = Administrator()
def main():
    @admin.bot.event
    async def on_ready():
        print('[bot] Logged in as {0} ({0.id})'.format(admin.bot.user))
        command_prefix = admin.config['command_prefix']
        print(f'[bot] Interact with it using the prefix \'{(command_prefix)}\'')
        print('[bot] Invite to your server with this link: {0}'.format('https://discord.com/api/oauth2/authorize?client_id=1010404496888840193&permissions=8&scope=bot'))

    for file in os.listdir('cogs'):
        if file.endswith(".py"):
            name = file[:-3]
            print(f"[init] Loading cogs.{name}")
            admin.bot.load_extension(f"cogs.{name}")
    dotenv.load_dotenv()
    admin.bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()