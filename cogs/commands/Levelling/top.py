import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_levelling import get_levelling_top
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="top", aliases=[], usage="")
    @commands.cooldown(1, 5, BucketType.guild)
    async def top(self, ctx):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        embed = discord.Embed(
            title="Levelling Top",
            description=str(await get_levelling_top(guild=ctx.guild)),
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "top benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(top(bot))
