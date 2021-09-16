import datetime

from discord.ext import commands

from cogs.core.config.config_general import config_fix
from cogs.core.functions.logging import log


class on_missing_config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_missing_config(self, message):
        time = datetime.datetime.now()
        await config_fix(guildid=message.guild.id)
        await log(
            text=f"{str(time)}: Der Bot hat die fehlende Config automatisch wiederhergestellt.",
            guildid=message.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_missing_config(bot))
