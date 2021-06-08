import json
import time
import os
import asyncio
import random
import qrcode
import re
import datetime
import discord
from urllib.request import urlopen
from discord.ext import commands


class functions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def get_prefix(bot, message):
    path = os.path.join('data', 'configs', f'{message.guild.id}.json')
    if not os.path.exists(path):
        with open(path, 'w') as f:
            data = {"prefix": "!",
                    "botchannel": "None",
                    "memechannel": "None",
                    "memesource": "memes",
                    "colour": 13372193}
            json.dump(data, f, indent=4)
            return commands.when_mentioned_or('!')(bot, message)
    with open(path, 'r') as f:
        data = json.load(f)
    prefix = str(data["prefix"])
    return commands.when_mentioned_or(prefix)(bot, message)


def get_prefix_string(message):
    path = os.path.join('data', 'configs', f'{message.guild.id}.json')
    if not os.path.exists(path):
        return str('!')
    with open(path, 'r') as f:
        data = json.load(f)
    prefix = str(data["prefix"])
    return str(prefix)


def get_botc(message):
    path = os.path.join('data', 'configs', f'{message.guild.id}.json')
    with open(path, 'r') as f:
        data = json.load(f)
    return data["botchannel"]


def get_memec(message):
    path = os.path.join('data', 'configs', f'{message.guild.id}.json')
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
    path = os.path.join('data', 'logs', f'{id}.txt')
    if os.path.isfile(path):
        with open(path, 'a') as f:
            f.write(input + '\n')
        if countlines(path=path) >= 250:
            deletelines(path=path, amount=1)
    else:
        with open(path, 'a') as f:
            f.write(input + '\n')


def get_author():
    Author = 'SimsumMC#3679'
    return Author


def get_botname():
    return str("Community Bot")


def get_colour(message):
    path = os.path.join('data', 'configs', f'{message.guild.id}.json')
    with open(path, 'r') as f:
        data = json.load(f)
    if data["colour"] == "random":
        return random_colour()
    return data["colour"]


def get_colour_code(colour):
    global final
    if colour == "Rot":
        final = 0xa80000
    elif colour == "Hellrot":
        final = 0xf00000
    elif colour == "Gelb":
        final = 0xf3d720
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
               "Grau", "Weiß", "Dunkellila", "Lila", "Pink", "bunt", "rainbow", "random", "Gelb"]
    if colour in colours:
        return True
    return False


def random_colour():
    colours = ["Rot", "Hellrot", "Hellblau", "Blau", "Gelb", "Hellgrün", "Grün", "Hellorange", "Orange", "Dunkellila",
               "Lila"
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
    return str("Nein")


def get_blacklist(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["blacklist"]
    else:
        with open(path, "w") as f:
            data = {
                "blacklist": []
            }
            json.dump(data, f, indent=4)
        return get_blacklist(path)


def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None


def redditnsfwcheck(reddit):
    url = f"https://www.reddit.com/r/{reddit}/about.json"
    response = urlopen(url)
    data = json.loads(response.read())
    if data["data"]["over18"] is True:
        return True
    return False


def get_memes(id):
    path = os.path.join('data', 'configs', f'{id}.json')
    with open(path, 'r+') as f:
        data = json.load(f)
    if 'memesource' in data:
        return data["memesource"]
    writejson("memesource", "memes", path)
    return "memes"


def readjson(type, path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data[type]


def get_checkedmemes(reddit):
    data = readjson(type="verified", path=os.path.join('data', 'verifiedmemes', 'memes.json'))
    if reddit in data:
        return False
    return False


def add_automaticdelete(id):
    time = 2592000000
    path = os.path.join('data', 'deletecache', 'delete_waiting.json')
    list = readjson("list", path)
    list.append(id)
    writejson(type="list", input=list, path=path)
    with open(path, 'r') as f:
        data = json.load(f)
    data["time"[id]] = time
    with open(path, 'w') as f:
        json.load(f)
        json.dump(data, f, indent=4)


def resetconfig(path):
    with open(path, 'w') as f:
        data = {"prefix": "!",
                "botchannel": "None",
                "memechannel": "None",
                "memesource": "memes",
                "colour": 13372193}
        json.dump(data, f, indent=4)
    return True


########################################################################################################################


def setup(bot):
    bot.add_cog(functions(bot))
