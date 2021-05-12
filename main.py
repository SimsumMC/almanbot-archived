import sys
import datetime
import traceback
import os
import discord
import asyncio
from discord.ext import commands
from commands.functions import get_prefix, msg_contains_word, get_blacklist, get_colour, get_prefix_string, get_author\
    , log


class CommunityBot(commands.Bot):

    async def on_ready(self):
        print('\n---------------------------------------------------------------------------------------------------\n')
        print(f'Der Bot mit dem Namen "{self.user}" wurde erfolgreich gestartet!')
        while True:
            await client.change_presence(activity=discord.Game('discord.visitlink.de'), status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game('Custom Prefixes'), status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game('Many Settings'), status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game('Open Source'), status=discord.Status.online)
            await asyncio.sleep(5)

    async def on_message(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        path = os.path.join('data', 'blacklist', f'{message.guild.id}.json')
        bannedWords = get_blacklist(path)
        if bannedWords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
            for bannedWord in bannedWords:
                if msg_contains_word(message.content.lower(), bannedWord):
                    await message.delete()
                    embed = discord.Embed(title='**Fehler**', description='Deine Nachricht hat ein verbotenes Wort '
                    'enthalten, daher wurde sie gelöscht. Sollte dies ein Fehler sein kontaktiere einen Administrator.'
                    , colour=get_colour(message=message))
                    embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                    await message.channel.send(embed=embed, delete_after=5)
                    log(str(time) + f': Der Spieler {user} hat versucht ein verbotenes Wort zu benutzen.'
                               ' Wort: "{bannedWord}"', message.guild.id)
                    break
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

client.run('token')
