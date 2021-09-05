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
from config import (
    COIN_HEAD,
    COIN_NUMBER,
)


class coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["münze", "coin", "münzwurf"])
    async def coinflip(self, ctx):
        global picture, strval
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            value = random.randint(1, 2)
            if value == 1:
                strval = "Kopf"
                picture = COIN_HEAD
            elif value == 2:
                strval = "Zahl"
                picture = COIN_NUMBER
            embed = discord.Embed(
                title="**Münzwurf**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=picture)
            embed.add_field(
                name="‎", value=f"Das Ergebnis ist ```{strval}```", inline=False
            )
            embed._footer = get_embed_footer(ctx)
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "münzwurf benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(coinflip(bot))
