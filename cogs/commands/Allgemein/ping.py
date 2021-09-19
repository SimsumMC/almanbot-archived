import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from main import client


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        ping = round(client.latency * 1000)
        if await botchannel_check(ctx):
            embed = discord.Embed(
                title="**Ping**", colour=await get_embedcolour(ctx.message)
            )
            embed.add_field(
                name="‎", value=f"Mein  Ping beträgt aktuell {ping}ms!", inline=False
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + f" hat sich den Ping ({str(ping)}ms) ausgeben lassen.",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(ping(bot))
