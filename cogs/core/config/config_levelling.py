import datetime
import json
import os

import discord
from discord.ext import commands
from easy_pil import Editor, Font
from easy_pil.loader import load_image_async

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer


class config_levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


user_cooldowns = {}


async def add_user_xp(message: discord.Message, xp: int, cooldown=True, messages=True):
    user = message.author
    guild = message.guild
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
            lvl_str = str(data["levelling"]["user"][str(user.id)]["level"])
            if lvl_str in data["levelling"]["roles"]:
                role = message.guild.get_role(data["levelling"]["roles"][lvl_str])
                try:
                    await message.author.add_roles(role)
                except Exception:
                    embed = discord.Embed(
                        title="Fehler",
                        description=f"Dem Nutzer {str(message.author)} konnte folgende Levelling-Rolle nicht gegeben werden: {role.name}!",
                        colour=await get_embedcolour(guild=message.guild),
                    )
                    embed._footer, embed._thumbnail = (
                        await get_embed_footer(
                            guild=message.guild, author=message.guild.owner
                        ),
                        await get_embed_thumbnail(),
                    )
                    await message.guild.owner.send(embed=embed)
            if messages:
                await send_lvl_up_message(
                    message, levelling_data=data["levelling"]["user"][str(user.id)]
                )
        else:
            break

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


async def send_lvl_up_message(message: discord.Message, levelling_data: dict):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    config = data["levelling"]["messages"]
    if not config["on"]:
        return
    desc = config["content"]
    if "{level}" in desc:
        desc = desc.replace("{level}", str(levelling_data["level"]))
    elif "{xp}" in desc:
        desc = desc.replace("{xp}", str(levelling_data["xp"]))
    elif "{old_level}" in desc:
        desc = desc.replace("{old_level}", str(levelling_data["level"] - 1))
    elif "{mention}" in desc:
        desc = desc.replace("{mention}", str(message.author.mention))
    elif "{name}" in desc:
        desc = desc.replace("{name}", str(message.author.name))
    embed = discord.Embed(
        title="Levelaufstieg", description=desc, colour=await get_embedcolour(message)
    )
    embed._footer = await get_embed_footer(message=message)
    embed._thumbnail = await get_embed_thumbnail()
    if config["mode"] == "same":
        await message.reply(embed=embed)
    elif config["mode"] == "dm":
        embed.description = desc + f"\n\nServer: {message.guild.name}"
        await message.author.send(embed=embed)
    elif config["mode"] == "channel":
        channel = message.guild.get_channel(config["channel"])
        await channel.send(embed=embed)


async def get_user_levelling_data(
    guild: discord.Guild, user: discord.Member = None, userid=None
) -> dict:
    userid = userid if userid else user.id
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    levelling_dict = data["levelling"]["user"]
    if str(userid) not in levelling_dict:
        data["levelling"]["user"][str(userid)] = {
            "xp": 0,
            "level": 0,
        }
    return data["levelling"]["user"][str(userid)]


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
        if not discord_user:
            user_data = await get_user_levelling_data(
                userid=int(user["id"]), guild=guild
            )
        else:
            user_data = await get_user_levelling_data(user=discord_user, guild=guild)
        top_string = (
            top_string
            + f"\n{passes}. {discord_user.mention if discord_user else '@<' + user['id'] + '>'} - Level: {user_data['level']} | XP: {user_data['xp']}"
        )
        passes += 1
    return top_string


async def levelling_active(guild: discord.Guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if data["levelling"]["active"]:
        return True
    return False


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
