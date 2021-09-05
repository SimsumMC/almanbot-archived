import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.logging import log
from config import CUBE


class wuerfel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="würfel")
    async def wuerfel(self, ctx, number1: int = 1, number2: int = 6):
        time = datetime.datetime.now()
        user = ctx.author.name
        value = random.randint(number1, number2)
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Würfel**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=CUBE)
            embed._footer = get_embed_footer(ctx)
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
