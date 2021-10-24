import os
import time

from discord.ext import commands, tasks

from cogs.core.config.config_giveaways import end_giveaway
from cogs.core.functions.func_json import readjson, writejson


class giveaway_check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_ended_giveaways.start()

    @tasks.loop(seconds=5)
    async def check_for_ended_giveaways(self):
        await self.bot.wait_until_ready()
        path = os.path.join("data", "cache", "giveaway_cache.json")
        actual_time = round(time.time())
        data = await readjson(key="giveaways", path=path)
        item, remove = 0, []
        for giveaway in data:
            if giveaway["unix_time"] <= actual_time:
                "passed"
                await end_giveaway(self.bot, giveaway)
                remove.append(giveaway)
            item += 1

        # get Actual data & remove Giveaways

        data: list = await readjson(key="giveaways", path=path)
        for item in remove:
            try:
                data.remove(item)
            except ValueError:
                pass
        await writejson(key="giveaways", value=data, path=path)


def setup(bot):
    bot.add_cog(giveaway_check(bot))
