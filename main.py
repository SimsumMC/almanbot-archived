import sys
import datetime
import traceback
import os
import discord
import platform
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded, Bot
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
    STATUS, TESTING_MODE,
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
        from cogs.commands.Allgemein.botinfo import (
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
        elif isinstance(message.channel, discord.DMChannel):
            Bot.dispatch(self, "dm_message", message)
            return
        elif not config_check(guildid=message.guild.id):
            Bot.dispatch(self, "missing_config", message)
        elif client.user.mentioned_in(message) and len(message.content) == len(f"<@!{client.user.id}>"):
            Bot.dispatch(self, "bot_mention", message)
        elif message.content in get_trigger_list(message.guild.id):
            Bot.dispatch(self, "trigger", message)
        Bot.dispatch(self, "blacklist_check", message)
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
                if filename.endswith(".py") and "ignore_" not in filename:
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
