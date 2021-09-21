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
        if data["levelling"]["user"][str(user.id)]["xp"] >= (
                data["levelling"]["user"][str(user.id)]["level"] + 1) * 100:
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


async def get_levelling_top(guild: discord.Guild):
    from main import client
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    levelling_dict = data["levelling"]["user"]
    top_list = []
    passes = 1
    top_string = ""
    for user in levelling_dict:
        user_dict = {
            "id": str(user),
            "xp": data["levelling"]["user"][str(user)]["xp"],
            "level": data["levelling"]["user"][str(user)]["level"]
        }
        top_list.append(user_dict)
    sorted_list_cache = sorted(top_list, key=lambda i: i["xp"], reverse=True)
    sorted_list = sorted(sorted_list_cache, key=lambda i: i["level"], reverse=True)[:10]

    for user in sorted_list:
        discord_user = client.get_user(int(user["id"]))
        user_data = await get_user_levelling_data(user=discord_user, guild=guild)
        top_string = top_string + f"\n{passes}. {discord_user.mention} - Level: {user_data['level']} | XP: {user_data['xp']}"
        passes += 1
    return top_string


########################################################################################################################


def setup(bot):
    bot.add_cog(config_levelling(bot))
