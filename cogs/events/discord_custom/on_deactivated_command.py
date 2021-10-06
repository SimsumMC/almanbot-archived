import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.ctx_utils import get_commandname
from cogs.core.functions.logging import log


class on_deactivated_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_deactivated_command(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = await get_commandname(ctx)
        await log(
            text=f"{time}: Der Nutzer {user} hat probiert den Befehl {await get_prefix_string(ctx.message)}"
            f"{str(ctx.command)} zu nutzen, dieser war aber auf dem Server deaktiviert!",
            guildid=ctx.guild.id,
        )
        embed = discord.Embed(
            title="**Fehler**",
            description=f"Der Befehl {name} ist auf diesem Server deaktiviert!",
            colour=await get_embedcolour(message=ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)


########################################################################################################################


def setup(bot):
    bot.add_cog(on_deactivated_command(bot))
