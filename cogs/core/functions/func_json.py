import json

from discord.ext import commands


class func_json(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def writejson(type, input, path, mode="write"):
    with open(path, "r") as f:
        data = json.load(f)
    if mode == "write":
        data[type] = input
    elif mode == "append":
        data[type].append(input)
    elif mode == "remove":
        data[type].remove(input)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def readjson(type, path):
    with open(path, "r") as f:
        data = json.load(f)
    return data[type]


########################################################################################################################


def setup(bot):
    bot.add_cog(func_json(bot))
