import json
import os
from shutil import copyfile

from discord.ext import commands


class config_general(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


# general Config things

def get_defaultconfig():
    data = {"prefix": "!",
            "botchannel": "None",
            "memechannel": "None",
            "memesource": "memes",
            "colour": 13372193,
            "trigger": [],
            "triggermsg": {}}
    return data


def config_check(guildid):
    path = os.path.join("data", "configs", f"{guildid}.json")
    if os.path.isfile(path):
        return True
    return False


def config_fix(guildid):
    path = os.path.join("data", "configs", f"{guildid}.json")
    pathcheck = os.path.join("data", "configs", "deleted", f"{guildid}.json")
    if os.path.isfile(pathcheck):
        copyfile(pathcheck, path)
        os.remove(pathcheck)
        return
    data = get_defaultconfig()
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def resetconfig(path):
    with open(path, 'w') as f:
        data = get_defaultconfig()
        json.dump(data, f, indent=4)
    return True


########################################################################################################################


def setup(bot):
    bot.add_cog(config_general(bot))
