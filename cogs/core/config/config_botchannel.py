import json
import os
from shutil import copyfile

from discord.ext import commands


class config_botchannel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


# botchannel Config things

def check_if_botcfg_actual(path):  # todo
    ...


def recreate_botcfg(path):  # todo
    ...


def check_if_botchannel(guildid, channelid, botchannelid):  # todo
    ...


def get_botchannel(path):  # todo
    ...


########################################################################################################################


def setup(bot):
    bot.add_cog(config_botchannel(bot))
