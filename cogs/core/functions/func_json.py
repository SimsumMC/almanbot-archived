import json

from discord.ext import commands


class func_json(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def writejson(key, value, path, mode="write"):
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    if mode == "write":
        data[key] = value
    elif mode == "append":
        data[key].append(value)
    elif mode == "remove":
        data[key].remove(value)
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


async def readjson(key: str, path):
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    if key in data:
        return True and data[key]
    return False and None


########################################################################################################################


def setup(bot):
    bot.add_cog(func_json(bot))
