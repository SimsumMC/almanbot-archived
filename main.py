import sys
import traceback
import os
import discord
from discord.ext import commands
from commands.functions import get_prefix


class CommunityBot(commands.Bot):

    async def on_ready(self):
        print(f'Der {self.user} wurde erfolgreich gestartet!')

    async def on_message(self, message):
        await self.process_commands(message)


########################################################################################################################


client = CommunityBot(command_prefix=get_prefix, help_command=None,
                      case_insensitive=True, intents=discord.Intents.all())

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        extension = f'commands.{filename[:-3]}'
        try:
            print(f'Der Command {extension} konnte erfolgreich geladen werden.')
            client.load_extension(extension)
        except Exception as e:
            print(f'Der Command "{extension}" konnte nicht geladen werden.', file=sys.stderr)
            traceback.print_exc()

client.run('ODEwOTMzMTI0NTk4NTk1NjE0.YCq2Uw.zwHKjgtDNhOpGixX7p-qUn7Qt9k')