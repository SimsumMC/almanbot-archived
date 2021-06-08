import sys
import datetime
import traceback
import os
import discord
import asyncio
from discord.ext import commands
from cogs.core.functions.functions import get_prefix, msg_contains_word, get_blacklist, get_colour, get_prefix_string, \
    get_author \
    , log
from discord_components import DiscordComponents


class CommunityBot(commands.Bot):

    async def on_ready(self):
        DiscordComponents(client)
        print('\n---------------------------------------------------------------------------------------------------\n')
        print(f'Der Bot mit dem Namen "{self.user}" wurde erfolgreich gestartet!')
        while True:
            await client.change_presence(activity=discord.Game('discord.visitlink.de'),
                                         status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game('Custom Prefixes'), status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game('Many Settings'), status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game('Open Source'), status=discord.Status.online)
            await asyncio.sleep(5)
            await client.change_presence(activity=discord.Game(f'in {len(client.guilds)} Servern'),
                                         status=discord.Status.online)
            await asyncio.sleep(5)

    async def on_message(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        path = os.path.join('data', 'blacklist', f'{message.guild.id}.json')
        bannedWords = get_blacklist(path)
        if message.author.bot:
            return
        elif client.user.mentioned_in(message) and len(message.content) == len(f"<@!{client.user.id}>"):
            embed = discord.Embed(title='**Prefix**', color=get_colour(message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name=' ⠀ ', value=f'Mein Prefix hier ist: ```{get_prefix_string(message)}```', inline=True)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            await message.channel.send(embed=embed)
            log(f"{time}: Der Spieler {user} hat sich den Prefix über eine Erwähnung ausgeben lassen.",
                message.guild.id)
        elif bannedWords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
            for bannedWord in bannedWords:
                if msg_contains_word(message.content.lower(), bannedWord):
                    if msg_contains_word(message.content.lower(), "blacklist add") or \
                            msg_contains_word(message.content.lower(), "blacklist remove") or \
                            msg_contains_word(message.content.lower(), "qr"):
                        pass
                    else:
                        await message.delete()
                        embed = discord.Embed(title='**Fehler**', description='Deine Nachricht hat ein verbotenes Wort '
                                                                              'enthalten, daher wurde sie gelöscht. '
                                                                              'Sollte dies ein Fehler sein '
                                                                              'kontaktiere einen Administrator. '
                                              , colour=get_colour(message=message))
                        embed.set_footer(
                            text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                                message=message),
                            icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                     '/winging-easy.png?width=676&height=676')
                        await message.channel.send(embed=embed, delete_after=5)
                        log(str(time) + f': Der Spieler {user} hat versucht ein verbotenes Wort zu benutzen.'
                                        ' Wort: "{bannedWord}"', message.guild.id)
                        return
        await self.process_commands(message)


########################################################################################################################


client = CommunityBot(command_prefix=get_prefix, help_command=None,
                      case_insensitive=True, intents=discord.Intents.all())

check = 0
for directory in os.listdir('./cogs'):
    for directory2 in os.listdir(f'./cogs/{directory}'):
        if check == 0:
            print(f"\n\nDirectory: {directory}/{directory2}\n")
        for filename in os.listdir(f'./cogs/{directory}/{directory2}/'):
            if filename.endswith('.py'):
                extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
                try:
                    client.load_extension(extension)
                    print(f'Das Modul {extension} konnte erfolgreich geladen werden.')
                except Exception as e:
                    print(f'Das Modul "{extension}" konnte nicht geladen werden.', file=sys.stderr)
                    traceback.print_exc()
        check = 0

client.run('test')
