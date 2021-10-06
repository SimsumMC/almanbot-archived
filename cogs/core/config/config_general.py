import json
import os
from shutil import copyfile
from config import (
    DEFAULT_PREFIX,
    DEFAULT_EMBEDCOLOUR,
    DEFAULT_MEMESOURCE,
    DEFAULT_TRIGGER,
    DEFAULT_TRIGGER_LIST,
    DEFAULT_BUTTONCOLOUR,
    DEFAULT_LEVELLING_COOLDOWN,
    DEFAULT_LEVELLING_XP_PER_MESSAGE,
    DEFAULT_LVLUP_MESSAGE,
    DEFAULT_LVLUP_MODE,
)
from discord.ext import commands


class config_general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# general Config things


async def get_defaultconfig():
    data = {
        "prefix": DEFAULT_PREFIX,
        "embedcolour": DEFAULT_EMBEDCOLOUR,
        "buttoncolour": DEFAULT_BUTTONCOLOUR,
        "memesource": DEFAULT_MEMESOURCE,
        "botchannel": [],
        "memechannel": [],
        "blacklist": [],
        "autoroles": [],
        "deactivated_commands": [],
        "trigger": {
            "triggerlist": DEFAULT_TRIGGER_LIST,
            "triggermsg": DEFAULT_TRIGGER,
        },
        "errors": {
            "command_not_found": False,
            "not_owner": True,
            "user_missing_permissions": True,
            "bot_missing_permissions": True,
            "missing_argument": True,
            "wrong_channel": True,
            "badargument": True,
            "command_on_cooldown": True,
            "not_nsfw_channel": True,
        },
        "welcome_messages": {"active": False, "channel": None, "style": {}},
        "leave_messages": {"active": False, "channel": None, "style": {}},
        "tags": {"list": [], "tagmsg": {}},
        "levelling": {
            "messages": {
                "on": True,
                "mode": DEFAULT_LVLUP_MODE,  # dm , channel, same
                "channel": None,
                "content": DEFAULT_LVLUP_MESSAGE,  # {level} {xp} {old_level} {mention} {name}
            },
            "active": True,
            "cooldown": DEFAULT_LEVELLING_COOLDOWN,
            "xp_per_message": DEFAULT_LEVELLING_XP_PER_MESSAGE,
            "user": {},
            "roles": {},
        },
    }
    return data


async def config_check(guildid):
    path = os.path.join("data", "configs", f"{guildid}.json")
    if os.path.isfile(path):
        return True
    return False


async def config_fix(guildid):
    path = os.path.join("data", "configs", f"{guildid}.json")
    pathcheck = os.path.join("data", "configs", "deleted", f"{guildid}.json")
    if os.path.isfile(pathcheck):
        copyfile(pathcheck, path)
        os.remove(pathcheck)
        return
    data = await get_defaultconfig()
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


async def resetconfig(guildid):
    path = os.path.join("data", "configs", f"{guildid}.json")
    os.remove(path=path)
    with open(path, "w") as f:
        data = await get_defaultconfig()
        json.dump(data, f, indent=4)
    return True


async def get_config(guildid):
    """
    :param guildid:
    :return: Guild-Config as Json
    """
    path = os.path.join("data", "configs", f"{guildid}.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data


########################################################################################################################


def setup(bot):
    bot.add_cog(config_general(bot))
