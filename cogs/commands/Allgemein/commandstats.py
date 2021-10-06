import datetime
import json
import os

import discord
import matplotlib.pyplot as plt
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.logging import log


class commandstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commandstats", aliases=["usage", "cmdstats"])
    async def commandstats(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name

        top_dict = await get_top_commands()
        y, x = [], []
        for command in top_dict:
            y.append(command["usages"])
            x.append(await get_name(self.bot, command["name"]))

        plt.bar(x, y)
        plt.xlabel("Anzahl der Nutzungen")
        plt.ylabel("Befehle")
        plt.savefig("diagram.png")
        plt.close()
        file = discord.File("diagram.png", filename="diagram.png")
        embed = discord.Embed(
            title="CommandStats", colour=await get_embedcolour(ctx.message)
        )
        embed.set_image(url="attachment://diagram.png")
        embed._footer = await get_embed_footer(ctx)
        await ctx.send(file=file, embed=embed)
        os.remove("diagram.png")
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "example benutzt!",
            guildid=ctx.guild.id,
        )


async def get_name(bot, command):
    if len(command) <= 5:
        return command
    command = bot.get_command(command)
    for alias in command.aliases:
        if len(alias) <= 5:
            return alias
    else:
        return command.name[:5]


async def get_top_commands():
    path = os.path.join("data", "cache", f"commandusage_cache.json")
    with open(path, "r") as f:
        data = json.load(f)
    dict_list = []
    for key in data:
        command_dict = {"name": key, "usages": data[key]}
        dict_list.append(command_dict)
    sorted_list = sorted(dict_list, key=lambda i: i["usages"], reverse=True)[:10]
    return sorted_list


########################################################################################################################


def setup(bot):
    bot.add_cog(commandstats(bot))
