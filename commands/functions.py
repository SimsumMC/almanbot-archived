import json
import os
import random
import qrcode
from discord.ext import commands


class functions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def get_prefix(bot, message):
    path = "data\\configs\\" + str(message.guild.id) + ".json"
    if not os.path.exists(path):
        with open(path, 'w') as f:
            data = {"prefix": "!",
                    "botchannel": "None",
                    "memechannel": "None",
                    "colour": 13372193}
            json.dump(data, f, indent=4)
            return commands.when_mentioned_or(prefix)(bot, message)
    else:
        with open(path, 'r') as f:
            data = json.load(f)
        prefix = str(data["prefix"])
        return commands.when_mentioned_or(prefix)(bot, message)


def get_prefix_string(message):
    path = "data\\configs\\" + str(message.guild.id) + ".json"
    if not os.path.exists(path):
        return str('!')
    else:
        with open(path, 'r') as f:
            data = json.load(f)
        prefix = str(data["prefix"])
        return str(prefix)


def get_botc(message):
    path = "data\\configs\\" + str(message.guild.id) + ".json"
    with open(path, 'r') as f:
        data = json.load(f)
    return str(data["botchannel"])


def get_memec(message):
    path = "data\\configs\\" + str(message.guild.id) + ".json"
    with open(path, 'r') as f:
        data = json.load(f)
    return data["memechannel"]


def countlines(path, mode='r+'):
    count = 0
    with open(path, mode) as f:
        for _ in f:
            count += 1
    return count


def deletelines(path, amount):
    initial_line = 1
    file_lines = {}

    with open(path) as f:
        content = f.readlines()

    for line in content:
        file_lines[initial_line] = line.strip()
        initial_line += 1

    f = open(path, "w")
    for line_number, line_content in file_lines.items():
        if line_number != amount:
            f.write('{}\n'.format(line_content))


def log(input, id):
    path = 'data\\logs\\' + str(id) + '.txt'
    if os.path.isfile(path):
        with open(path, 'a') as f:
            f.write(input + '\n')
        if countlines(path=path) > 250:
            deletelines(path=path, amount=1)
    else:
        with open(path, 'w') as f:
            pass
        with open(path, 'a') as f:
            f.write(input + '\n')


def get_author():
    Author = 'SimsumMC#3679'
    return Author


def get_botname():
    return str("Community Bot")


def get_colour(message):
    path = "data\\configs\\" + str(message.guild.id) + ".json"
    with open(path, 'r') as f:
        data = json.load(f)
    if data["colour"] == "random":
        return random_colour()
    else:
        return data["colour"]


def get_colour_code(colour):
    global final
    if colour == "Rot":
        final = 0xa80000
    elif colour == "Hellrot":
        final = 0xf00000
    elif colour == "Hellblau":
        final = 0x2fa5ee
    elif colour == "Blau":
        final = 0x573ce2
    elif colour == "Hellgrün":
        final = 0x20de12
    elif colour == "Grün":
        final = 0x41a13a
    elif colour == "Hellorange":
        final = 0xe29455
    elif colour == "Orange":
        final = 0xe36d0d
    elif colour == "Schwarz":
        final = 0x000000
    elif colour == "Hellgrau":
        final = 0x999494
    elif colour == "Grau":
        final = 0x444141
    elif colour == "Weiß":
        final = 0xffffff
    elif colour == "Dunkellila":
        final = 0x852598
    elif colour == "Lila":
        final = 0xb144e4
    elif colour == "Pink":
        final = 0xe114bc
    elif colour == "bunt" or colour == "rainbow" or colour == "random":
        final = "random"
    else:
        final = 13372193
    return final


def colour_check(colour):
    colours = ["Rot", "Hellrot", "Hellblau", "Blau", "Hellgrün", "Grün", "Hellorange", "Orange", "Schwarz", "Hellgrau",
               "Grau", "Weiß", "Dunkellila", "Lila", "Pink", "bunt", "rainbow", "random"]
    if colour in colours:
        return True
    else:
        return False


def random_colour():
    colours = ["Rot", "Hellrot", "Hellblau", "Blau", "Hellgrün", "Grün", "Hellorange", "Orange", "Dunkellila", "Lila"
               , "Pink"]
    return get_colour_code(random.choice(colours))


def writejson(type, input, path):
    with open(path, 'r') as f:
        data = json.load(f)
    data[type] = input
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def is_not_pinned(message):
    return not message.pinned


def make_qr(filename, msg):
    img = qrcode.make(msg)
    img.save(filename)


def whoisr(member):
    if member.bot is True:
        return str("Ja")
    else:
        return str("Nein")

def get_blacklist(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["blacklist"]
    else:
        with open(path, "r+") as f:
            data = {
                "blacklist": []
            }
            json.dump(data, f, indent=4)
        return get_blacklist(path)


def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None


########################################################################################################################


def setup(bot):
    bot.add_cog(functions(bot))
