import json
import os
import random

from discord.ext import commands


class config_colours(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_colour(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if data["colour"] == "random":
        return random_colour()
    return data["colour"]


def get_colour_code(colour):
    global final
    if colour == "Rot":
        final = 0xA80000
    elif colour == "Hellrot":
        final = 0xF00000
    elif colour == "Gelb":
        final = 0xF3D720
    elif colour == "Hellblau":
        final = 0x2FA5EE
    elif colour == "Blau":
        final = 0x573CE2
    elif colour == "Hellgrün":
        final = 0x20DE12
    elif colour == "Grün":
        final = 0x41A13A
    elif colour == "Hellorange":
        final = 0xE29455
    elif colour == "Orange":
        final = 0xE36D0D
    elif colour == "Schwarz":
        final = 0x000000
    elif colour == "Hellgrau":
        final = 0x999494
    elif colour == "Grau":
        final = 0x444141
    elif colour == "Weiß":
        final = 0xFFFFFF
    elif colour == "Dunkellila":
        final = 0x852598
    elif colour == "Lila":
        final = 0xB144E4
    elif colour == "Pink":
        final = 0xE114BC
    elif colour == "bunt" or colour == "rainbow" or colour == "random":
        final = "random"
    else:
        final = 13372193
    return final


def colour_check(colour):
    colours = [
        "Rot",
        "Hellrot",
        "Hellblau",
        "Blau",
        "Hellgrün",
        "Grün",
        "Hellorange",
        "Orange",
        "Schwarz",
        "Hellgrau",
        "Grau",
        "Weiß",
        "Dunkellila",
        "Lila",
        "Pink",
        "bunt",
        "rainbow",
        "random",
        "Gelb",
    ]
    if colour in colours:
        return True
    return False


def random_colour():
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
    return get_colour_code(random.choice(colours))


########################################################################################################################


def setup(bot):
    bot.add_cog(config_colours(bot))


