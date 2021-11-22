import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button

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
                embed=embed, components=await get_calculator_buttons(ctx.message)
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


async def on_calculator_button(interaction):
    user = interaction.user
    description = str(interaction.message.embeds[0].description)[:-3][3:]
    if description == CALCULATING_ERROR + "|":
        description = "|"
    elif (
        len(description) != 1
        and interaction.component.label == "x"
        and description[-2] == "x"
    ):
        pass
    elif interaction.component.label == "Exit":
        default_button_array = await get_calculator_buttons(interaction.message)
        final_button_array, cache_array = [], []
        for array in default_button_array:
            for button in array:
                button._disabled = True
                cache_array.append(button)
            final_button_array.append(cache_array)
            cache_array = []
        await interaction.respond(
            type=7,
            content="Rechner geschlossen!",
            components=final_button_array,
        )
        return
    elif interaction.component.label == "⌫":
        description = description[:-2] + "|"
    elif interaction.component.label == "Clear":
        description = "|"
    elif interaction.component.label == "=":
        description = str(await calculate(description[:-1])) + "|"
    else:
        description = description[:-1] + interaction.component.label + "|"
    description = "```" + description + "```"
    embed = discord.Embed(
        title=f"**{interaction.author.name}'s Rechner**",
        description=description,
        colour=await get_embedcolour(interaction.message),
    )
    embed._footer = await get_embed_footer(
        message=interaction.message, author=interaction.author
    )
    await interaction.respond(
        type=7,
        embed=embed,
        components=await get_calculator_buttons(interaction.message),
    )
    await log(
        f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Rechner-Nachricht interagiert!",
        interaction.message.guild.id,
    )


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
