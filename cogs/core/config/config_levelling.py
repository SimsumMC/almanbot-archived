import datetime
import json
import os

import discord
from discord.ext import commands
from easy_pil import Editor, Font
from easy_pil.loader import load_image_async


class config_levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


user_cooldowns = {}


async def add_user_xp(
    user: discord.Member, guild: discord.Guild, xp: int, cooldown=True
):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    levelling_dict = data["levelling"]["user"]
    if str(user.id) not in levelling_dict:
        data["levelling"]["user"][str(user.id)] = {
            "xp": 0,
            "level": 0,
        }
    if cooldown and await get_user_cooldown(user, guild) != 0:
        return
    data["levelling"]["user"][str(user.id)]["xp"] += xp
    await add_user_cooldown(
        user, guild, cooldown=dict(await get_levelling_config(guild))["cooldown"]
    )
    while True:
        if (
            data["levelling"]["user"][str(user.id)]["xp"]
            >= (data["levelling"]["user"][str(user.id)]["level"] + 1) * 100
        ):
            data["levelling"]["user"][str(user.id)]["level"] += 1
            data["levelling"]["user"][str(user.id)]["xp"] = data["levelling"]["user"][
                str(user.id)
            ]["xp"] - (data["levelling"]["user"][str(user.id)]["level"] * 100)
        else:
            break
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


async def get_user_levelling_data(user: discord.Member, guild: discord.Guild) -> dict:
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


async def get_levelling_top(guild: discord.Guild) -> str:
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
            "level": data["levelling"]["user"][str(user)]["level"],
        }
        top_list.append(user_dict)
    sorted_list_cache = sorted(top_list, key=lambda i: i["xp"], reverse=True)
    sorted_list = sorted(sorted_list_cache, key=lambda i: i["level"], reverse=True)[:10]

    for user in sorted_list:
        discord_user = client.get_user(int(user["id"]))
        user_data = await get_user_levelling_data(user=discord_user, guild=guild)
        top_string = (
            top_string
            + f"\n{passes}. {discord_user.mention} - Level: {user_data['level']} | XP: {user_data['xp']}"
        )
        passes += 1
    return top_string


async def add_user_cooldown(user: discord.Member, guild: discord.Guild, cooldown: int):
    time = int(datetime.datetime.now().timestamp())
    if not str(user.id) in user_cooldowns:
        user_cooldowns[str(user.id)] = {}
    user_cooldowns[str(user.id)][str(guild.id)] = time + cooldown


async def get_user_cooldown(user: discord.Member, guild: discord.Guild) -> int:
    time = int(datetime.datetime.now().timestamp())
    if not str(user.id) in user_cooldowns:
        user_cooldowns[str(user.id)] = {}
    if str(guild.id) not in user_cooldowns[str(user.id)]:
        return 0
    cooldown = int(user_cooldowns[str(user.id)][str(guild.id)]) - time
    return cooldown if cooldown >= 0 else 0


async def get_levelling_config(guild: discord.Guild) -> dict:
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data["levelling"]


async def get_rank_card(member: discord.Member, guild: discord.Guild):
    name_lenght = len(str(member))
    underline = int(name_lenght * 27) if name_lenght <= 13 else int(name_lenght * 25)
    user_data = await get_user_levelling_data(user=member, guild=guild)
    level = user_data["level"]
    xp = user_data["xp"]
    xp_for_next_level = (user_data["level"] + 1) * 100
    progress = int((xp / xp_for_next_level) * 100)
    print(progress)
    background = Editor(os.path.join("data", "pictures", "rank_card.png"))
    image = await load_image_async(str(member.avatar_url))
    profile = Editor(image).resize((190, 190)).circle_image()

    poppins = Font().poppins(size=40)
    poppins_small = Font().poppins(size=30)

    background.paste(profile, (50, 50))

    background.rectangle((290, 220), width=650, height=40, fill="#494b4f", radius=20)
    if float(progress) > 5:
        background.bar(
            (290, 220),
            max_width=650,
            height=40,
            percentage=progress if progress > 5 else 0,
            fill="#6FF31F",
            radius=20,
        )
    background.text((290, 40), str(member), font=poppins, color="white")

    background.rectangle((290, 100), width=underline, height=2, fill="#86EB48")
    background.text(
        (290, 125),
        f"Level : {level}\nXP : {xp} / {xp_for_next_level}",
        font=poppins_small,
        color="white",
    )
    return background.image_bytes


########################################################################################################################


def setup(bot):
    bot.add_cog(config_levelling(bot))
