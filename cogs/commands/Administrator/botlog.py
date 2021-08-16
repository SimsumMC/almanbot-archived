import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class botlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def botlog(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join("data", "logs", f"{ctx.guild.id}.txt")
        if botchannel_check(ctx):
            if os.path.isfile(path):
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat sich den Log mit der ID "'
                    + str(ctx.guild.id)
                    + '" ausgeben lassen!',
                    id=ctx.guild.id,
                )
                await ctx.author.send(file=discord.File(path))
                embed = discord.Embed(
                    title="**Erfolgreich**",
                    description="Schau in deine Privatnachrichten!",
                    colour=get_embedcolour(ctx.message),
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
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
            else:
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
                    value="Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster "
                    "Befehl ist!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat sich probiert den noch nicht existierenden Log mit der ID "'
                    + str(ctx.guild.id)
                    + '" ausgeben zu lassen!',
                    id=ctx.guild.id,
                )

        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "serverlog im Channel #"
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

    @botlog.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
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
                value="Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um "
                + get_prefix_string(ctx.message)
                + "botlog zu nutzen.",
                id=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(botlog(bot))
