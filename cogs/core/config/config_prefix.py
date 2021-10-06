import json
import os

from discord.ext import commands

from cogs.core.config.config_general import get_defaultconfig
from config import DEFAULT_PREFIX


class config_prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_prefix_string(message=None, guild=None) -> str:
    if guild:
        guildid = guild.id
    else:
        guildid = message.guild.id
    path = os.path.join("data", "configs", f"{guildid}.json")
    if not os.path.exists(path):
        return str(DEFAULT_PREFIX)
    with open(path, "r") as f:
        data = json.load(f)
    prefix = str(data["prefix"][0])
    return str(prefix)


async def get_prefix(bot, message) -> commands.when_mentioned_or():
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            data = await get_defaultconfig()
            json.dump(data, f, indent=4)
            return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    with open(path, "r") as f:
        data = json.load(f)
    prefix = str(data["prefix"][0])
    return commands.when_mentioned_or(prefix)(bot, message)


########################################################################################################################


def setup(bot):
    bot.add_cog(config_prefix(bot))
