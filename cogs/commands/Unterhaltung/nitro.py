import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour


class nitro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nitro")
    async def nitro(self, ctx):
        embed = discord.Embed(title="**Nitro**", colour=get_embedcolour(message=ctx.message))
        ...


########################################################################################################################

def setup(bot):
    bot.add_cog(nitro(bot))
