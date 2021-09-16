import json
import os
import random

from discord.ext import commands

from config import DEFAULT_EMBEDCOLOUR, EMBEDCOLOUR_CODES, EMBEDCOLOURS_SUPPORTED


class config_colours(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_embedcolour(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if data["embedcolour"] == "random":
        return await random_embedcolour()
    return data["embedcolour"]


async def get_embedcolour_code(colour):
    colour_codes = EMBEDCOLOUR_CODES
    if colour_codes[colour.lower()]:
        return True and colour_codes[colour.lower()]
    return False and DEFAULT_EMBEDCOLOUR


async def embedcolour_check(colour):
    colours = EMBEDCOLOURS_SUPPORTED
    if colour.lower() in colours:
        return True
    return False


async def random_embedcolour():
    colours = [
        "Rot",
        "Hellrot",
        "Hellblau",
        "Blau",
        "Gelb",
        "Hellgrün",
        "Grün",
        "Hellorange",
        "Orange",
        "Dunkellila",
        "Lila",
        "Pink",
    ]
    return await get_embedcolour_code(random.choice(colours))


async def colourcode_to_name(code):
    for name, colourcode in EMBEDCOLOUR_CODES.items():
        if colourcode == code:
            return name.capitalize()
########################################################################################################################


def setup(bot):
    bot.add_cog(config_colours(bot))
