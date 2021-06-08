import time
import os
from discord.ext import commands
from cogs.core.functions.functions import readjson, writejson


class automaticdelete(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def check_delete_waiting(list, times, path):
    x = 1
    for id in list:
        times[id] -= 3600000
        if int(times[id]) <= 3600000:
            x += 1
            del times[id]
            list.remove(id)
    if x > 1:
        writejson(type="time", input=times, path=path)


def main():
    while True:
        time.sleep(2592000)
        path = os.path.join('data', 'deletecache', 'delete_waiting.json')
        list = readjson("list", path)
        times = readjson("time", path)
        check_delete_waiting(list, times, path)


########################################################################################################################

def setup(bot):
    bot.add_cog(automaticdelete(bot))
