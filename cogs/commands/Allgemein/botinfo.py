import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from config import (
    BOT_MAIN_DEVELOPER,
    BOT_DEVELOPERLIST,
    GITHUB_LINK,
    WEBSITE_LINK,
    ABOUT,
)
from main import client


def get_developer_string():
    if len(BOT_DEVELOPERLIST) == 1:
        return BOT_MAIN_DEVELOPER
    return "".join([dev + " ," for dev in BOT_DEVELOPERLIST])[:-1]


def get_member_count():
    ergebnis = 0
    for guild in client.guilds:
        ergebnis += guild.member_count
    return int(ergebnis)


class botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo", aliases=["info", "about", "bot"])
    async def botinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Botinfo**",
                description=ABOUT,
                color=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            embed.add_field(
                name="**Entwickler**", value=get_developer_string(), inline=True
            )
            embed.add_field(name="**Projektbeginn**", value="Anfang 2021", inline=True)
            embed.add_field(name="**Arbeitszeit**", value="ca. 50 Stunden", inline=True)
            embed.add_field(
                name="**Server**", value=f"{len(client.guilds)}", inline=True
            )
            embed.add_field(
                name="**Nutzer**", value=f"{get_member_count()}", inline=True
            )
            embed.add_field(
                name="**Source**",
                value=f"[Github]({GITHUB_LINK})",
                inline=True,
            )
            embed.add_field(
                name="**Website**",
                value=f"[Link]({WEBSITE_LINK})",
                inline=True,
            )
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl  "
                + get_prefix_string(ctx.message)
                + "botinfo benutzt!",
                ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(botinfo(bot))
