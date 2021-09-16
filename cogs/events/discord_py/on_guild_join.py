import datetime
import json
import os
from shutil import copyfile

from discord.ext import commands

from cogs.core.config.config_general import get_defaultconfig
from cogs.core.functions.logging import log
from config import TESTING_MODE, TESTING_GUILDS


class on_guild_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if TESTING_MODE is True:
            if guild.id not in TESTING_GUILDS:
                await guild.leave()
                print(
                    f"TEST_MODE is True! Left server with ID {guild.id} and Name {guild.name} "
                    f"because it was not marked as a testing server."
                )
                return
        path = os.path.join("data", "configs", f"{guild.id}.json")
        pathcheck = os.path.join("data", "configs", "deleted", f"{guild.id}.json")
        # config
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
        else:
            with open(path, "w") as f:
                data = get_defaultconfig()
                json.dump(data, f, indent=4)
        # logs
        path = os.path.join("data", "logs", f"{guild.id}.txt")
        pathcheck = os.path.join("data", "logs", "deleted", f"{guild.id}.txt")
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
            await log(
                f"{datetime.datetime.now()}: Der Bot ist dem Server erneut beigetreten.",
                guild.id,
            )
        else:
            await log(
                f"{datetime.datetime.now()}: Der Bot ist dem Server beigetreten.",
                guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_guild_join(bot))
