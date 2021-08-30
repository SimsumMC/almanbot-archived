import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import BadArgument, Bot

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, CUBE, WRONG_CHANNEL_ERROR


class wuerfel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="würfel")
    async def wuerfel(self, ctx, number1: int = 1, number2: int = 6):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        value = random.randint(number1, number2)
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Würfel**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=CUBE)
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎", value=f"Du hast eine ```{value}``` gewürfelt!", inline=False
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat eine "
                + str(value)
                + " gewürfelt.",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(wuerfel(bot))
