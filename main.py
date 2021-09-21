import os
import platform
import sys
import traceback
from asyncio import sleep

import discord
from discord.ext import commands
from discord.ext.commands import Bot, ExtensionAlreadyLoaded
from discord_components import DiscordComponents

from cogs.core.config.config_general import config_check
from cogs.core.config.config_levelling import add_user_xp
from cogs.core.config.config_prefix import get_prefix, get_prefix_string
from cogs.core.config.config_trigger import get_trigger_list
from cogs.core.functions.func_json import readjson
from cogs.core.functions.functions import msg_contains_word
from config import (
    DISCORD_TOKEN,
    BANNER,
    ACTIVITY_LIST,
    STATUS,
    BLACKLIST_IGNORE,
    TESTING_MODE,
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


async def blacklist_check(self, message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    bannedWords = await readjson(key="blacklist", path=path)
    if bannedWords:
        if TESTING_MODE is not True:
            if message.author.id == message.guild.owner_id:
                return False
        for bannedWord in bannedWords:
            if await msg_contains_word(message.content.lower(), bannedWord):
                for ignorearg in BLACKLIST_IGNORE:
                    if await msg_contains_word(await get_prefix_string(message) + message.content.lower(), ignorearg):
                        return False
                else:
                    Bot.dispatch(
                        self, "blacklist_word", message, bannedword=bannedWord
                    )
                    return True


########################################################################################################################

class AlmanBot(commands.Bot):
    async def on_ready(self):
        DiscordComponents(client)
        print(BANNER)
        print("\n----------------------------------------------------------------\n")
        print(f'Der Bot mit dem Namen "{self.user}" wurde erfolgreich gestartet!\n')
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Operating System: {platform.system()} {platform.release()} ({os.name})")
        client.loop.create_task(self.status_task())

    async def status_task(self):
        from cogs.commands.Allgemein.botinfo import (
            get_member_count,
            get_developer_string,
        )

        while True:
            for activity in ACTIVITY_LIST:
                if "{guild_count}" in activity:
                    activity = activity.replace(
                        "{guild_count}", str(len(client.guilds))
                    )
                elif "{user_count}" in activity:
                    activity = activity.replace("{user_count}", str(await get_member_count()))
                elif "{developer_names}" in activity:
                    activity = activity.replace(
                        "{developer_names}", str(await get_developer_string())
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
        elif not await config_check(guildid=message.guild.id):
            Bot.dispatch(self, "missing_config", message)
        elif client.user.mentioned_in(message) and len(message.content) == len(
                f"<@!{client.user.id}>"
        ):
            Bot.dispatch(self, "bot_mention", message)
        elif await blacklist_check(self, message):
            return
        elif message.content in await get_trigger_list(message.guild.id):
            Bot.dispatch(self, "trigger", message)
        await add_user_xp(user=message.author, guild=message.guild, xp=5)
        await self.process_commands(message)


########################################################################################################################


client = AlmanBot(
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
    "cogs.core.config.config_levelling",
]

for extension in most_important:
    client.load_extension(extension)

check = 0
for directory in os.listdir("./cogs"):
    for directory2 in os.listdir(f"./cogs/{directory}"):
        if directory2 == "Ignore":
            continue
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
