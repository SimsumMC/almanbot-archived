import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int, channel: discord.TextChannel = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            try:
                if channel is None:
                    await ctx.channel.edit(slowmode_delay=seconds)
                    channel = str(ctx.channel.mention)
                    channelname = ctx.channel.name
                else:
                    await channel.edit(slowmode_delay=seconds)
                    channel = channel.mention
                    channelname = channel.name
                embed = discord.Embed(
                    title="**Slowmode**", colour=get_embedcolour(ctx.message)
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
                embed.add_field(
                    name="⠀",
                    value=f"Der Slowmode vom Channel {channel} wurde zu {seconds} Sekunden geändert.",
                )
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat im Chat "#'
                    + str(channelname)
                    + '" den Slowmode'
                    f" auf {seconds} Sekunden gesetzt.",
                    guildid=ctx.guild.id,
                )
            except Exception:
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
                    value="Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + ": Der Bot hatte nicht die nötigen Berrechtigungen um "
                    + get_prefix_string(ctx.message)
                    + "slowmode auszuführen..",
                    guildid=ctx.guild.id,
                )
        else:
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "slowmode im Channel #"
                + str(name)
                + " zu benutzen!",
                guildid=ctx.guild.id,
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

    @slowmode.error
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
                value="Dir fehlt folgende Berrechtigung um den Befehl auszuführen: "
                "```manage_channels```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um "
                + get_prefix_string(ctx.message)
                + "slowmode zu nutzen.",
                guildid=ctx.guild.id,
            )
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
                + "slowmode <Sekunden> <opt. Channel>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "slowmode eingegeben.",
                guildid=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(slowmode(bot))
