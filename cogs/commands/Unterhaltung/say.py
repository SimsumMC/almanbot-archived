import asyncio
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR, THUMBNAIL_URL


class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, text):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            await ctx.send(content=str(text), components=[[
                    Button(style=get_buttoncolour(message=ctx.message), label="Normal", emoji="📄", id="say_normal", disabled=True),
                    Button(style=get_buttoncolour(message=ctx.message), label="Embed", emoji="✒", id="say_embed"),
                                                         ]],
                           )
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "ssp benutzt!",
                id=ctx.guild.id,
            )

        else:
            log(
                input=str(time)
                      + ": Der Spieler "
                      + str(user)
                      + " hat probiert den Befehl "
                      + get_prefix_string(ctx.message)
                      + "say im Channel #"
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

    @say.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
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
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                      + get_prefix_string(ctx.message)
                      + "say <das was ich sagen soll>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                      + ": Der Spieler "
                      + str(user)
                      + " hat nicht alle erforderlichen Argumente beim Befehl "
                      + get_prefix_string(ctx.message)
                      + "say eingegeben.",
                id=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(say(bot))
