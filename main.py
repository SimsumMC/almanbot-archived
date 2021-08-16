import sys
import datetime
import traceback
import os
import discord
import platform
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded
from cogs.core.functions.func_json import readjson
from cogs.core.functions.functions import msg_contains_word, get_author
from cogs.core.config.config_prefix import get_prefix_string, get_prefix
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from cogs.core.config.config_trigger import get_trigger_list, get_trigger_msg
from discord_components import DiscordComponents
from cogs.core.config.config_general import config_check, config_fix
from config import (
    DISCORD_TOKEN,
    ICON_URL,
    THUMBNAIL_URL,
    FOOTER,
    BANNER,
    ACTIVITY_LIST,
    STATUS,
)


########################################################################################################################


def run_check():
    version = sys.version_info
    if not int(version.major) >= 3 and int(version.minor) >= 7:
        if int(version.major) == 4:
            return
        raise SystemExit(
            f"Du brauchst eine aktuellere Python Version um das Skript auszuführen, mindestens 3.7 oder höher!"
        )
    return


run_check()


########################################################################################################################


class CommunityBot(commands.Bot):
    async def on_ready(self):
        DiscordComponents(client)
        print(BANNER)
        print(
            "\n---------------------------------------------------------------------------------------------------\n"
        )
        print(f'Der Bot mit dem Namen "{self.user}" wurde erfolgreich gestartet!\n')
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        client.loop.create_task(self.status_task())

    async def status_task(self):
        from cogs.commands.Informationen.botinfo import (
            get_member_count,
            get_developer_string,
        )

        while True:
            for activity in ACTIVITY_LIST:
                if "{guild_count}" in activity:
                    activity = activity.replace("{guild_count}", str(len(client.guilds)))
                elif "{user_count}" in activity:
                    activity = activity.replace("{user_count}", str(get_member_count()))
                elif "{developer_names}" in activity:
                    activity = activity.replace(
                        "{developer_names}", str(get_developer_string())
                    )
                await client.change_presence(
                    activity=discord.Game(activity),
                    status=STATUS,
                )
                await sleep(5)

    async def on_message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            embed = discord.Embed(title="Hinweis | Note", colour=0xF00000)
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.add_field(
                name="German",
                value="Dieser Bot hat keine DM Funktion - daher bringt es nichts "
                "mich hier zu kontaktieren.",
                inline=False,
            )
            embed.add_field(
                name="English",
                value="This bot don't have a DM Function - so you cant achieve something "
                "with writing something to me.",
                inline=False,
            )
            embed.set_footer(
                text=f"{FOOTER[0]}{message.author.name}{FOOTER[1]}{str(get_author())}{FOOTER[2]}undefined",
                icon_url=ICON_URL,
            )
            await message.channel.send(embed=embed)
            return
        time = datetime.datetime.now()
        ignore = ["blacklist add", "blacklist remove", "qr"]
        user = message.author.name
        path = os.path.join("data", "configs", f"{message.guild.id}.json")
        if not config_check(guildid=message.guild.id):  # todo make it working lmao
            config_fix(guildid=message.guild.id)
            log(
                input=f"{str(time)}: Der Bot hat die fehlende Config automatisch wiederhergestellt.",
                id=message.guild.id,
            )
        bannedWords = readjson(type="blacklist", path=path)
        if client.user.mentioned_in(message) and len(message.content) == len(
            f"<@!{client.user.id}>"
        ):
            embed = discord.Embed(title="**Prefix**", color=get_embedcolour(message))
            embed.set_footer(
                text=FOOTER[0]
                + message.author.name
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(message)),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name=" ⠀ ",
                value=f"Mein Prefix hier ist: ```{get_prefix_string(message)}```",
                inline=True,
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            await message.channel.send(embed=embed)
            log(
                f"{time}: Der Spieler {user} hat sich den Prefix über eine Erwähnung ausgeben lassen.",
                message.guild.id,
            )
        elif message.content in get_trigger_list(
            message.guild.id
        ):  # trigger check + msg
            answer = get_trigger_msg(guildid=message.guild.id, trigger=message.content)
            if answer is not None:
                embed = discord.Embed(
                    title="**Trigger**",
                    description=answer,
                    color=get_embedcolour(message),
                )
                embed.set_footer(
                    text="for "
                    + str(user)
                    + " | by "
                    + str(get_author())
                    + " | Prefix "
                    + str(get_prefix_string(message)),
                    icon_url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739"
                    "/winging-easy.png?width=676&height=676",
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                await message.channel.send(embed=embed)
        elif bannedWords != [] and ():  # check if word in blacklist
            for bannedWord in bannedWords:
                if msg_contains_word(message.content.lower(), bannedWord):
                    for ignorearg in ignore:
                        if msg_contains_word(message.content.lower(), ignorearg):
                            return
                    else:
                        await message.delete()
                        embed = discord.Embed(
                            title="**Fehler**",
                            description="Deine Nachricht hat ein verbotenes Wort "
                            "enthalten, daher wurde sie gelöscht. "
                            "Sollte dies ein Fehler sein "
                            "kontaktiere einen Administrator des "
                            "Servers. ",
                            colour=get_embedcolour(message=message),
                        )
                        embed.set_footer(
                            text=FOOTER[0]
                            + message.author.name
                            + FOOTER[1]
                            + str(get_author())
                            + FOOTER[2]
                            + str(get_prefix_string(message)),
                            icon_url=ICON_URL,
                        )
                        await message.channel.send(embed=embed, delete_after=5)
                        log(
                            str(time)
                            + f": Der Spieler {user} hat versucht ein verbotenes Wort zu benutzen."
                            ' Wort: "{bannedWord}"',
                            message.guild.id,
                        )
                        return
        await self.process_commands(message)


########################################################################################################################


client = CommunityBot(
    command_prefix=get_prefix,
    help_command=None,
    case_insensitive=True,
    intents=discord.Intents.all(),
)


########################################################################################################################


most_important = [
    "cogs.core.functions.functions",
    "cogs.core.config.config_botchannel",
    "cogs.core.config.config_memechannel",
]
for extension in most_important:
    client.load_extension(extension)

check = 0
for directory in os.listdir("./cogs"):
    if directory != "Ignore":
        for directory2 in os.listdir(f"./cogs/{directory}"):
            if check == 0:
                print(f"\n\nDirectory: {directory}/{directory2}\n")
            for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                if filename.endswith(".py"):
                    extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
                    try:
                        client.load_extension(extension)
                        print(
                            f"Das Modul {extension} konnte erfolgreich geladen werden."
                        )
                    except ExtensionAlreadyLoaded:
                        pass
                    except Exception:
                        print(
                            f'Das Modul "{extension}" konnte nicht geladen werden.',
                            file=sys.stderr,
                        )
                        traceback.print_exc()
            check = 0


########################################################################################################################


client.run(DISCORD_TOKEN)
