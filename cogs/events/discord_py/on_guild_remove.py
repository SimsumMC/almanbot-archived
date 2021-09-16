import os
from shutil import copyfile

from discord.ext import commands

from config import TESTING_MODE, TESTING_GUILDS


class on_guild_remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if TESTING_MODE and guild.id not in TESTING_GUILDS:
            return
        path = os.path.join("data", "configs", f"{guild.id}.json")
        path2 = os.path.join("data", "logs", f"{guild.id}.txt")
        dest = os.path.join("data", "configs", "deleted", f"{guild.id}.json")
        dest2 = os.path.join("data", "logs", "deleted", f"{guild.id}.txt")
        copyfile(path, dest)
        copyfile(path2, dest2)
        os.remove(path)
        os.remove(path2)


########################################################################################################################


def setup(bot):
    bot.add_cog(on_guild_remove(bot))
