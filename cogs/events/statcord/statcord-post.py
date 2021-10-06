import json
import os

import statcord
from discord.ext import commands

from config import STATCORD_TOKEN


class statcordpost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if STATCORD_TOKEN != "statcord token":
            self.key = STATCORD_TOKEN
            self.api = statcord.Client(self.bot, self.key)
            self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await save_command_usage(ctx)
        await save_invoke_by_author(ctx)
        if STATCORD_TOKEN != "statcord token":
            self.api.command_run(ctx)


async def save_command_usage(ctx):
    command = (
        str(ctx.command)
        if " " not in str(ctx.command)
        else str(ctx.command).split(" ")[0]
    )
    path = os.path.join("data", "cache", f"commandusage_cache.json")
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    if command not in data:
        data[command] = 0
    data[command] += 1
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


async def save_invoke_by_author(ctx):
    path = os.path.join("data", "cache", f"commandamount_user_cache.json")
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    if str(ctx.author.id) not in data:
        data[str(ctx.author.id)] = 0
    data[str(ctx.author.id)] += 1
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def setup(bot):
    bot.add_cog(statcordpost(bot))
