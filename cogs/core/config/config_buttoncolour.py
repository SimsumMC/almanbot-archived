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


def get_buttoncolour(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if data["buttoncolour"] == "random":
        return random_buttoncolour()
    return transform_to_colour_class(data["buttoncolour"])


def transform_to_colour_class(buttoncolour: str):  # "green"  # red, blue, grey
    data = {
        "green": ButtonStyle.green,
        "red": ButtonStyle.red,
        "blue": ButtonStyle.blue,
        "grey": ButtonStyle.grey,
    }
    if data[buttoncolour]:
        return True and data[buttoncolour]
    return False and transform_to_colour_class(DEFAULT_BUTTONCOLOUR)


def buttoncolour_check(colour):
    global colours
    if colour in colours:
        return True
    return False


def random_buttoncolour():
    global colours
    return transform_to_colour_class(random.choice(colours))


########################################################################################################################


def setup(bot):
    bot.add_cog(config_buttoncolour(bot))
