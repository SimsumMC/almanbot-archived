import json
import os

from discord.ext import commands

from cogs.core.config.config_general import get_defaultconfig
from config import DEFAULT_PREFIX


class config_prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_prefix_string(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    if not os.path.exists(path):
        return str("!")
    with open(path, "r") as f:
        data = json.load(f)
    prefix = str(data["prefix"])
    return str(prefix)


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


########################################################################################################################


def setup(bot):
    bot.add_cog(config_prefix(bot))
