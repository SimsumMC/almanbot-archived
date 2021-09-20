import os

from discord.ext import commands

from cogs.core.config.config_botchannel import get_botchannel
from cogs.core.config.config_memechannel import get_memechannel
from cogs.core.functions.func_json import writejson


class on_guild_channel_delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_guild_channel_delete")
    async def on_guild_channel_delete(self, channel):
        path = os.path.join("data", "configs", f"{channel.guild.id}.json")
        if channel.id in await get_botchannel(message=channel):
            await writejson(
                key="botchannel", value=channel.id, path=path, mode="remove"
            )
        elif channel.id in await get_memechannel(message=channel):
            await writejson(
                key="memechannel", value=channel.id, path=path, mode="remove"
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_guild_channel_delete(bot))
