import sys
import traceback
import os
import discord
import asyncio
from discord.ext import commands
from commands.functions import get_prefix


class CommunityBot(commands.Bot):

    async def on_ready(self):
        print('\n---------------------------------------------------------------------------------------------------\n')
        print(f'Der Bot mit dem Namen "{self.user}" wurde erfolgreich gestartet!')
        while True:
            await client.change_presence(activity=discord.Game('discord.visitlink.de'), status=discord.Status.online)
            await asyncio.sleep(2)
            await client.change_presence(activity=discord.Game('Custom Prefixes'), status=discord.Status.online)
            await asyncio.sleep(2)
            await client.change_presence(activity=discord.Game('Many Settings'), status=discord.Status.online)
            await asyncio.sleep(2)
            await client.change_presence(activity=discord.Game('Open Source'), status=discord.Status.online)
            await asyncio.sleep(2)

    async def on_message(self, message):
        await self.process_commands(message)


########################################################################################################################


client = CommunityBot(command_prefix=get_prefix, help_command=None,
                      case_insensitive=True, intents=discord.Intents.all())

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        extension = f'commands.{filename[:-3]}'
        try:
            print(f'Das Modul {extension} konnte erfolgreich geladen werden.')
            client.load_extension(extension)
        except Exception as e:
            print(f'Das Modul "{extension}" konnte nicht geladen werden.', file=sys.stderr)
            traceback.print_exc()

client.run('your token')
