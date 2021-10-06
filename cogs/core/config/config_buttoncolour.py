import json
import os
import random

from discord.ext import commands
from discord_components import ButtonStyle

from config import DEFAULT_BUTTONCOLOUR


class config_buttoncolour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


colours = ["red", "green", "blue", "grey"]


async def get_buttoncolour(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if data["buttoncolour"] == "random":
        return await random_buttoncolour()
    return await transform_to_colour_int(data["buttoncolour"])


async def transform_to_colour_int(buttoncolour: str):
    data = {
        "green": ButtonStyle.green,
        "red": ButtonStyle.red,
        "blue": ButtonStyle.blue,
        "grey": ButtonStyle.grey,
    }
    if data[buttoncolour]:
        return True and data[buttoncolour]
    return False and await transform_to_colour_int(DEFAULT_BUTTONCOLOUR)


async def buttoncolour_check(colour):
    global colours
    if colour in colours:
        return True
    return False


async def random_buttoncolour():
    global colours
    return await transform_to_colour_int(random.choice(colours))


async def translate_buttoncolour(language: str, colour: str = DEFAULT_BUTTONCOLOUR):
    if language == "de":
        translations = {
            "green": "Grün",
            "red": "Rot",
            "blue": "Blau",
            "grey": "Grau",
        }
        return translations[colour]
    elif language == "en":
        translations = {
            "grün": "green",
            "rot": "red",
            "blau": "blue",
            "grau": "grey",
        }
        return translations[colour]


async def get_button_colour_list(language):
    if language == "en":
        return ["green", "red", "blue", "grey"]
    else:
        return ["grün", "rot", "blau", "grau"]


########################################################################################################################


def setup(bot):
    bot.add_cog(config_buttoncolour(bot))
