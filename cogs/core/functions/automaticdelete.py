import json
import time
import os
from discord.ext import commands
from cogs.core.functions.func_json import writejson, readjson


class automaticdelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# TODO needs complete rewrite


########################################################################################################################


def setup(bot):
    bot.add_cog(automaticdelete(bot))
