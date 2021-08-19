import datetime

import discord
from discord.ext import commands
from discord_components import Button, DiscordComponents

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.cache import save_message_to_cache
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR, CALCULATING_ERROR


def calculate(calculation):
    o = calculation.replace('x', "*").replace('÷', '/')
    try:
        result = str(eval(o))
    except Exception:
        result = CALCULATING_ERROR
    return result


class calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calculator", aliases=["rechner", "calc"])
    async def calculator(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            embed = discord.Embed(
                title=f"**{ctx.author.name}'s Rechner**", description='```|```', colour=get_embedcolour(ctx.message)
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
            msg = await ctx.send(embed=embed, components=[
                [
                    Button(style=get_buttoncolour(message=ctx.message), label="1", id="calc_1"),
                    Button(style=get_buttoncolour(message=ctx.message), label="2", id="calc_2"),
                    Button(style=get_buttoncolour(message=ctx.message), label="3", id="calc_3"),
                    Button(style=get_buttoncolour(message=ctx.message), label="x", id="calc_x"),
                    Button(style=get_buttoncolour(message=ctx.message), label="Exit", id="calc_exit"),
                ],
                [
                    Button(style=get_buttoncolour(message=ctx.message), label="4", id="calc_4"),
                    Button(style=get_buttoncolour(message=ctx.message), label="5", id="calc_5"),
                    Button(style=get_buttoncolour(message=ctx.message), label="6", id="calc_6"),
                    Button(style=get_buttoncolour(message=ctx.message), label="÷", id="calc_division"),
                    Button(style=get_buttoncolour(message=ctx.message), label="⌫", id="calc_delete"),
                ],
                [
                    Button(style=get_buttoncolour(message=ctx.message), label="7", id="calc_7"),
                    Button(style=get_buttoncolour(message=ctx.message), label="8", id="calc_8"),
                    Button(style=get_buttoncolour(message=ctx.message), label="9", id="calc_9"),
                    Button(style=get_buttoncolour(message=ctx.message), label="+", id="calc_addition"),
                    Button(style=get_buttoncolour(message=ctx.message), label="Clear", id="calc_clear"),
                ],
                [
                    Button(style=get_buttoncolour(message=ctx.message), label="00", id="calc_00"),
                    Button(style=get_buttoncolour(message=ctx.message), label="0", id="calc_0"),
                    Button(style=get_buttoncolour(message=ctx.message), label=".", id="calc_comma"),
                    Button(style=get_buttoncolour(message=ctx.message), label="-", id="calc_subtraction"),
                    Button(style=get_buttoncolour(message=ctx.message), label="=", id="calc_equal"),
                ], ],
                           )
            await save_message_to_cache(msg)
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "rechner benutzt!",
                id=ctx.guild.id,
            )
        else:
            log(
                input=str(time)
                      + ": Der Spieler "
                      + str(user)
                      + " hat probiert den Befehl "
                      + get_prefix_string(ctx.message)
                      + "rechner im Channel #"
                      + str(name)
                      + " zu benutzen!",
                id=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
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
    bot.add_cog(calculator(bot))
    DiscordComponents(bot)
