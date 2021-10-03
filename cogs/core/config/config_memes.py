import json
import os

import aiohttp
from discord.ext import commands

from cogs.core.functions.func_json import writejson, readjson


class config_memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_memes(id):
    path = os.path.join("data", "configs", f"{id}.json")
    with open(path, "r+") as f:
        data = json.load(f)
    if "memesource" in data:
        return data["memesource"]
    await writejson("memesource", "memes", path)
    return "memes"


async def redditnsfwcheck(reddit):
    url = f"https://www.reddit.com/r/{reddit}/about.json"
    async with aiohttp.ClientSession() as session:
        async with session.request("GET", url) as response:
            data = await response.json()
            if data["data"]["over18"] is True:
                return True
            return False


async def meme_is_checked(reddit):
    data = await readjson(
        key="verified", path=os.path.join("data", "cache", "reddit_cache.json")
    )
    if reddit in data:
        return True
    return False


########################################################################################################################


def setup(bot):
    bot.add_cog(config_memes(bot))
