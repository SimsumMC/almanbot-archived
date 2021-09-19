import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class papier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def papier(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            papier = [
                "Ich hatte auch das Papier, Unentschieden!",
                "Du hast gewonnen, ich hatte mich für den Stein entschieden!",
                "Guter Versuch, aber ich habe aber mit der Schere gewonnen! Papier ist leider nur so dünn...",
            ]
            papierrandom = random.choice(papier)
            embed = discord.Embed(
                title="**Schere Stein Papier**",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(name="‎", value=str(papierrandom), inline=False)
            await ctx.send(embed=embed)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + await get_prefix_string(ctx.message)
                + "papier benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(papier(bot))
