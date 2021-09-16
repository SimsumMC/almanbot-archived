import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, DiscordComponents

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.cache import save_message_to_cache
from cogs.core.functions.logging import log
from config import CALCULATING_ERROR


async def calculate(calculation):
    o = calculation.replace("x", "*").replace("÷", "/")
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
        msg2 = ctx.message
        if await botchannel_check(ctx):
            embed = discord.Embed(
                title=f"**{ctx.author.name}'s Rechner**",
                description="```|```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            msg = await ctx.send(
                embed=embed,
                components=await get_calculator_buttons(ctx.message)
            )
            await save_message_to_cache(message=msg, author=msg2.author)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + await get_prefix_string(msg)
                + "rechner benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


async def get_calculator_buttons(message):
    buttoncolour = await get_buttoncolour(message)
    array = [
        [
            Button(
                style=buttoncolour,
                label="1",
                id="calc_1",
            ),
            Button(
                style=buttoncolour,
                label="2",
                id="calc_2",
            ),
            Button(
                style=buttoncolour,
                label="3",
                id="calc_3",
            ),
            Button(
                style=buttoncolour,
                label="x",
                id="calc_x",
            ),
            Button(
                style=buttoncolour,
                label="Exit",
                id="calc_exit",
            ),
        ],
        [
            Button(
                style=buttoncolour,
                label="4",
                id="calc_4",
            ),
            Button(
                style=buttoncolour,
                label="5",
                id="calc_5",
            ),
            Button(
                style=buttoncolour,
                label="6",
                id="calc_6",
            ),
            Button(
                style=buttoncolour,
                label="÷",
                id="calc_division",
            ),
            Button(
                style=buttoncolour,
                label="⌫",
                id="calc_delete",
            ),
        ],
        [
            Button(
                style=buttoncolour,
                label="7",
                id="calc_7",
            ),
            Button(
                style=buttoncolour,
                label="8",
                id="calc_8",
            ),
            Button(
                style=buttoncolour,
                label="9",
                id="calc_9",
            ),
            Button(
                style=buttoncolour,
                label="+",
                id="calc_addition",
            ),
            Button(
                style=buttoncolour,
                label="Clear",
                id="calc_clear",
            ),
        ],
        [
            Button(
                style=buttoncolour,
                label="00",
                id="calc_00",
            ),
            Button(
                style=buttoncolour,
                label="0",
                id="calc_0",
            ),
            Button(
                style=buttoncolour,
                label=".",
                id="calc_comma",
            ),
            Button(
                style=buttoncolour,
                label="-",
                id="calc_subtraction",
            ),
            Button(
                style=buttoncolour,
                label="=",
                id="calc_equal",
            ),
        ],
    ]
    return array


########################################################################################################################


def setup(bot):
    bot.add_cog(calculator(bot))
    DiscordComponents(bot)
