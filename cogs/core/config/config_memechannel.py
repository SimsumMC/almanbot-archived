import json
import os
from main import client
from discord.ext import commands


class config_memechannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Memechannel


async def memechannel_check(ctx):
    channelid = ctx.channel.id
    message = ctx.message
    ids = await get_memechannel(message=message)
    if channelid in ids or ids == []:
        return True
    return False


async def get_memechannel(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data["memechannel"]


async def get_memechannel_obj_list(ctx):
    memechannel = await get_memechannel(ctx.message)
    if not memechannel:
        return False
    string = "".join([client.get_channel(id).mention + ", " for id in memechannel])[:-2]
    return True and str(string)


########################################################################################################################


def setup(bot):
    bot.add_cog(config_memechannel(bot))
