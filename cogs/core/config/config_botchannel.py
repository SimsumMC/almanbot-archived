import json
import os
from main import client
from discord.ext import commands


class config_botchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Botchannel


async def botchannel_check(ctx):
    channelid = ctx.channel.id
    message = ctx.message
    ids = await get_botchannel(message=message)
    if ids == [] or channelid in ids:
        return True
    return False


async def get_botchannel(message):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data["botchannel"]


async def get_botchannel_obj_list(ctx):
    botchannel = await get_botchannel(ctx.message)
    if not botchannel:
        return False
    string = " ".join(
        [client.get_channel(channel).mention + ", " for channel in botchannel]
    )[:-2]
    return True and str(string)


########################################################################################################################


def setup(bot):
    bot.add_cog(config_botchannel(bot))
