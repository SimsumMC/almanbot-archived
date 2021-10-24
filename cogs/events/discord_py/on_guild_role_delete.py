import os

from discord.ext import commands
from cogs.core.config.config_memechannel import get_memechannel
from cogs.core.functions.func_json import writejson, readjson


class on_guild_role_delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_guild_role_delete")
    async def on_guild_role_delete(self, role):
        path = os.path.join("data", "configs", f"{role.guild.id}.json")
        levelling_dict = await readjson(path=path, key="levelling")
        roles: dict = levelling_dict["roles"]
        levelling_roles = roles.values()
        autoroles: list = await readjson(path=path, key="autoroles")
        if role.id in levelling_roles:
            key = dict((v, k) for k, v in roles.items()).get(role.id)
            del levelling_dict["roles"][key]
            await writejson(key="levelling", value=levelling_dict, path=path)
        elif role.id in autoroles:
            await writejson(key="autoroles", value=role.id, path=path, mode="remove")


########################################################################################################################


def setup(bot):
    bot.add_cog(on_guild_role_delete(bot))
