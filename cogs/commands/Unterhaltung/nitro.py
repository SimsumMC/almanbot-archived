import discord
from discord.ext import commands
from discord_components import Button

from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour


class nitro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nitro")
    async def nitro(self, ctx):
        embed = discord.Embed(
            title="**Ein Wi**", colour=await get_embedcolour(message=ctx.message)
        )
        await ctx.send(embed=embed, components=[
            Button(
                style=await get_buttoncolour(ctx.message),
                label="    Akzeptieren    ",
                custom_id="help_allgemein",
            )
        ])


########################################################################################################################


def setup(bot):
    bot.add_cog(nitro(bot))
