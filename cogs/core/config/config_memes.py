import json
import os
from urllib.request import urlopen

from discord.ext import commands

from cogs.core.functions.func_json import writejson, readjson


class config_memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_memes(id):
    path = os.path.join("data", "configs", f"{id}.json")
    with open(path, "r+") as f:
        data = json.load(f)
    if "memesource" in data:
        return data["memesource"]
    writejson("memesource", "memes", path)
    return "memes"


def redditnsfwcheck(reddit):
    url = f"https://www.reddit.com/r/{reddit}/about.json"
    response = urlopen(url)
    data = json.loads(response.read())
    if data["data"]["over18"] is True:
        return True
    return False


def meme_is_checked(reddit):
    data = readjson(
        type="verified", path=os.path.join("data", "cache", "reddit_cache.json")
    )
    if reddit in data:
        return True
    return False


########################################################################################################################


def setup(bot):
    bot.add_cog(config_memes(bot))
