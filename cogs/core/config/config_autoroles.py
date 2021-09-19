import os

from discord.ext import commands
import discord

from cogs.core.functions.func_json import readjson


class config_autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_role_objects(guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    roles = await readjson(key="autoroles", path=path)
    roleobjects = []
    for role in roles:
        roleobjects.append(discord.Guild.get_role(guild, role))
    return roleobjects


async def get_role_mentions_list(guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    roles = await readjson(key="autoroles", path=path)
    roleobjects = ""
    for role in roles:
        roleobjects = roleobjects + discord.Guild.get_role(guild, role).mention + ", "
    return roleobjects[:-2]


########################################################################################################################


def setup(bot):
    bot.add_cog(config_autoroles(bot))
