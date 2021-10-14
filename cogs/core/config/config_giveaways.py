import json
import os

import discord
from discord.ext import commands

from cogs.core.functions.func_json import readjson, writejson


class config_general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# giveaway Config things

async def create_giveaway(message_id, author_id, channel_id, winner_amount, prize, unix_time, guild: discord.Guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if "giveaways" not in data:
        data["giveaways"] = {}
    giveaway_dict = {
        "message_id": message_id,
        "channel_id": channel_id,
        "unix_time": unix_time,
        "winner_amount": winner_amount,
        "author_id": author_id,
        "prize": prize,
        "active": True,
        "member": [],
    }
    data["giveaways"][str(message_id)] = giveaway_dict
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)
    print(giveaway_dict)
    giveaway_dict["guild_id"] = guild.id
    del giveaway_dict["member"]
    del giveaway_dict["active"]
    print(giveaway_dict)
    await writejson(key="giveaways", value=giveaway_dict, mode="append", path=os.path.join("data", "cache", "giveaway_cache.json"))


async def add_giveaway_member(message: discord.Message, user: discord.Member):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if user.id not in data["giveaways"][str(message.id)]["member"]:
        data["giveaways"][str(message.id)]["member"].append(user.id)
        with open(path, "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)
        return True
    return False


########################################################################################################################


def setup(bot):
    bot.add_cog(config_general(bot))
