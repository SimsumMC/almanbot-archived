import sys
import datetime
import traceback
import os
import discord
from asyncio import sleep
from discord.ext import commands

from cogs.core.functions.functions import get_prefix, msg_contains_word, get_blacklist, get_colour, get_prefix_string, \
    get_author, log
from cogs.core.config.config_trigger import get_trigger_list, get_trigger_msg
from discord_components import DiscordComponents

from cogs.core.config.config_general import config_check, config_fix


def run_check():
    version = sys.version_info
    if not int(version.major) >= 3 and int(version.minor) >= 7:
        raise SystemExit(f"Du brauchst eine aktuellere Python Version um das Skript auszuführen, 3.7 oder höher!")
    return


run_check()


class CommunityBot(commands.Bot):

    async def on_ready(self):
        DiscordComponents(client)
        print('\n---------------------------------------------------------------------------------------------------\n')
        print(f'Der Bot mit dem Namen "{self.user}" wurde erfolgreich gestartet!')
        client.loop.create_task(self.status_task())

    async def status_task(self):
        while True:
            await client.change_presence(activity=discord.Game('discord.visitlink.de'),
                                         status=discord.Status.online)
            await sleep(5)
            await client.change_presence(activity=discord.Game('Custom Prefixes'), status=discord.Status.online)
            await sleep(5)
            await client.change_presence(activity=discord.Game('Many Settings'), status=discord.Status.online)
            await sleep(5)
            await client.change_presence(activity=discord.Game('Open Source'), status=discord.Status.online)
            await sleep(5)
            await client.change_presence(activity=discord.Game(f'in {len(client.guilds)} Guilds'),
                                         status=discord.Status.online)
            await sleep(5)

    async def on_message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            embed = discord.Embed(title='Hinweis | Note', colour=0xf00000)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            embed.add_field(name='German', value='Dieser Bot hat keine DM Funktion - daher bringt es nichts '
                                                 'mich hier zu kontaktieren.', inline=False)
            embed.add_field(name='English', value="This bot don't have a DM Function - so you cant achieve something "
                                                  "with writing something to me.", inline=False)
            embed.set_footer(text=f'for {message.author.name} | by ' + str(get_author()) + ' | Prefix undefined'
                             , icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                        '/803322491480178739/winging-easy.png?width=676&height=676')
            await message.channel.send(embed=embed)
            return
        time = datetime.datetime.now()
        ignore = ["blacklist add", "blacklist remove", "qr"]
        user = message.author.name
        path = os.path.join('data', 'blacklist', f'{message.guild.id}.json')
        bannedWords = get_blacklist(path)
        if not config_check(guildid=message.guild.id):  # todo make it working lmao
            print("try")
            config_fix(guildid=message.guild.id)
            log(input=f"{time}: Der Bot hat die fehlende Config automatisch wiederhergestellt.",
                id=message.guild.id)
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
        elif message.content in get_trigger_list(message.guild.id):  # trigger check + msg
            answer = get_trigger_msg(guildid=message.guild.id, trigger=message.content)
            embed = discord.Embed(title='**Trigger**', description=answer, color=get_colour(message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            await message.channel.send(embed=embed)
        elif bannedWords is not None and (
                isinstance(message.channel, discord.channel.DMChannel) is False):  # check if word in blacklist
            for bannedWord in bannedWords:
                if msg_contains_word(message.content.lower(), bannedWord):
                    for ignorearg in ignore:
                        if msg_contains_word(message.content.lower(), ignorearg):
                            return
                    else:
                        await message.delete()
                        embed = discord.Embed(title='**Fehler**', description='Deine Nachricht hat ein verbotenes Wort '
                                                                              'enthalten, daher wurde sie gelöscht. '
                                                                              'Sollte dies ein Fehler sein '
                                                                              'kontaktiere einen Administrator des '
                                                                              'Servers. '
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
    if directory != "Ignore":
        for directory2 in os.listdir(f'./cogs/{directory}'):
            if check == 0:
                print(f"\n\nDirectory: {directory}/{directory2}\n")
            for filename in os.listdir(f'./cogs/{directory}/{directory2}/'):
                if filename.endswith('.py'):
                    extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
                    try:
                        client.load_extension(extension)
                        print(f'Das Modul {extension} konnte erfolgreich geladen werden.')
                    except Exception:
                        print(f'Das Modul "{extension}" konnte nicht geladen werden.', file=sys.stderr)
                        traceback.print_exc()
            check = 0

client.run('ODEwOTMzMTI0NTk4NTk1NjE0.YCq2Uw.CvlJMR5Cndj5kYf3FaxhszvGQaI')
