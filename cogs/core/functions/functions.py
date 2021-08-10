import json
import os
import re

from discord.ext import commands

from cogs.core.config.config_general import get_defaultconfig
from config import BOT_MAIN_DEVELOPER, BOT_NAME, DEFAULT_PREFIX


class functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_prefix(bot, message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            data = get_defaultconfig()
            json.dump(data, f, indent=4)
            return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    with open(path, "r") as f:
        data = json.load(f)
    prefix = str(data["prefix"])
    return commands.when_mentioned_or(prefix)(bot, message)


def get_prefix_string(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    if not os.path.exists(path):
        return str("!")
    with open(path, "r") as f:
        data = json.load(f)
    prefix = str(data["prefix"])
    return str(prefix)


def get_author():
    return str(BOT_MAIN_DEVELOPER)


def get_botname():
    return str(BOT_NAME)


def writejson(type, input, path):
    with open(path, "r") as f:
        data = json.load(f)
    data[type] = input
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def is_not_pinned(message):
    return not message.pinned


def whoisr(member):
    if member.bot is True:
        return str("Ja")
    return str("Nein")


def get_blacklist(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["blacklist"]


def msg_contains_word(msg, word):
    return re.search(fr"\b({word})\b", msg) is not None


def readjson(type, path):
    with open(path, "r") as f:
        data = json.load(f)
    return data[type]


########################################################################################################################


def setup(bot):
    bot.add_cog(functions(bot))
