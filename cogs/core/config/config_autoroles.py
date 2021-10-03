import os

from discord.ext import commands
import discord

from cogs.core.functions.func_json import readjson


class config_autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_autorole_mentions_list(guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    roles = await readjson(key="autoroles", path=path)
    roleobjects = ""
    for role in roles:
        roleobjects = roleobjects + discord.Guild.get_role(guild, role).mention + ", "
    if roleobjects == "":
        return "Keine Autoroles eingestellt."
    return roleobjects[:-2]


async def get_autoroles(guild: discord.Guild):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    roles = await readjson(key="autoroles", path=path)
    role_objects = []
    for role in roles:
        role_objects.append(guild.get_role(role))
    return role_objects


########################################################################################################################


def setup(bot):
    bot.add_cog(config_autoroles(bot))
