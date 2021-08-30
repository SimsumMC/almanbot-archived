import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, SSP, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class schere(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schere(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            schere = [
                "Ich hatte auch die Schere, Unentschieden!",
                "Du hast gewonnen, ich hatte mich für das Papier entschieden!",
                "Guter Versuch, aber ich habe aber mit dem Stein gewonnen!",
            ]
            schererandom = random.choice(schere)
            embed = discord.Embed(
                title="**Schere Stein Papier**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=SSP)
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(name="‎", value=str(schererandom), inline=False)
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "schere benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(schere(bot))
