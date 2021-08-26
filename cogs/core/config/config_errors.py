import os

from discord.ext import commands

from cogs.core.functions.func_json import readjson


class config_errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def check_if_error(ctx, error):
    path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
    data = readjson(path=path, type="errors")
    if data[error] is True:
        return True
    return False


########################################################################################################################


def setup(bot):
    bot.add_cog(config_errors(bot))
