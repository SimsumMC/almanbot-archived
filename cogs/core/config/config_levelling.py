import json
import os

import discord
from discord.ext import commands


class config_levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def add_user_xp(user: discord.Member, guild: discord.Guild, xp: int):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    levelling_dict = data["levelling"]["user"]
    if str(user.id) not in levelling_dict:
        data["levelling"]["user"][str(user.id)] = {
            "xp": 0,
            "level": 0,
        }
    data["levelling"]["user"][str(user.id)]["xp"] += xp
    while True:
        if data["levelling"]["user"][str(user.id)]["xp"] >= (data["levelling"]["user"][str(user.id)]["level"] + 1) * 100:
            data["levelling"]["user"][str(user.id)]["level"] += 1
            data["levelling"]["user"][str(user.id)]["xp"] = \
                data["levelling"]["user"][str(user.id)]["xp"] - (data["levelling"]["user"][str(user.id)]["level"] * 100)
        else:
            break
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


async def get_user_levelling_data(user: discord.Member, guild: discord.Guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    levelling_dict = data["levelling"]["user"]
    if str(user.id) not in levelling_dict:
        data["levelling"]["user"][str(user.id)] = {
            "xp": 0,
            "level": 0,
        }
    return data["levelling"]["user"][str(user.id)]


########################################################################################################################


def setup(bot):
    bot.add_cog(config_levelling(bot))
