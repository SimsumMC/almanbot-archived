import datetime
import random
import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, COIN_HEAD, COIN_NUMBER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
)
from cogs.core.config.config_colours import get_colour
from cogs.core.functions.logging import log


class coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["münze", "coin", "münzwurf"])
    async def coinflip(self, ctx):
        global picture, strval
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            value = random.randint(1, 6)
            if value == 1:
                strval = "Kopf"
                picture = COIN_HEAD
            elif value == 2:
                strval = "Zahl"
                picture = COIN_NUMBER
            embed = discord.Embed(title="**Münzwurf**", colour=get_colour(ctx.message))
            embed.set_thumbnail(url=picture)
            embed.add_field(
                name="‎", value=f"Das Ergebnis ist ```{strval}```", inline=False
            )
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Spieler {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "münzwurf benutzt!",
                id=ctx.guild.id,
            )
        else:
            log(
                input=f"{time}: Der Spieler {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                f"münzwurf im Channel #{name} zu benutzen!",
                id=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**", description=WRONG_CHANNEL_ERROR, colour=get_colour(message=ctx.message)
            )
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
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(coinflip(bot))
