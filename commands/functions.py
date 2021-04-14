import datetime
import json
import os

import discord
import asyncio

from discord.ext import commands
from discord.ext.commands import CommandNotFound


class functions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def get_prefix(bot, message):
    path = "data\\configs\\" + str(message.guild.id) + ".json"
    if not os.path.exists(path):
        return commands.when_mentioned_or('!')(bot, message)
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
    Author = 'SimsumMC#0001'
    return Author


def writejson(type, input, path):
    with open(path, 'r') as f:
        data = json.load(f)
    data[type] = str(input)
    #os.remove(filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


########################################################################################################################


def setup(bot):
    bot.add_cog(functions(bot))