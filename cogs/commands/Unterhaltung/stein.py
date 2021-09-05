import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.logging import log
from config import SSP


class stein(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stein(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            stein = [
                "Ich hatte auch den Stein, Unentschieden!",
                "Du hast gewonnen, ich hatte mich für die Schere entschieden!",
                "Guter Versuch, aber ich habe aber mit dem Papier gewonnen!",
            ]
            steinrandom = random.choice(stein)
            embed = discord.Embed(
                title="**Schere Stein Papier**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=SSP)
            embed._footer = get_embed_footer(ctx)
            embed.add_field(name="‎", value=str(steinrandom), inline=False)
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "stein benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(stein(bot))
