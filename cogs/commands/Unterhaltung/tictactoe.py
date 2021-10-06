import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class tictactoe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tictactoe", aliases=["ttt"])
    @commands.is_owner()
    async def tictactoe(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        components = await get_ttt_buttons(ctx=ctx, default=True)
        print(components)
        embed = discord.Embed(
            title="TicTacToe",
            description="Klick einfach auf einen Button, wo du setzen möchtest! Du hast die Farbe `Rot`.",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed, components=components)
        await log(
            f"{time}: Der Nutzer {user} a!hat den Befehl {await get_prefix_string(ctx.message)}"
            "tictactoe benutzt!",
            guildid=ctx.guild.id,
        )


async def get_ttt_buttons(
    ctx=None, message=None, disabled=False, default=False, interaction=None
):
    global buttons
    if ctx:
        message = ctx.message
    if default:
        style = 2
        buttons = [
            [
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_0",
                ),
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_1",
                ),
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_2",
                ),
            ],
            [
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_3",
                ),
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_4",
                ),
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_5",
                ),
            ],
            [
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_6",
                ),
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_7",
                ),
                Button(
                    style=style,
                    label="     ",
                    custom_id="ttt_default_8",
                ),
            ],
        ]
        if disabled:
            final_button_array, cache_array = [], []
            for array in buttons:
                for button in array:
                    button._disabled = True
                    cache_array.append(button)
                final_button_array.append(cache_array)
                cache_array = []
            buttons = final_button_array
    return buttons


########################################################################################################################


def setup(bot):
    bot.add_cog(tictactoe(bot))
