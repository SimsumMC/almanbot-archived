import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log


class slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slowmode", usage="<Sekunden> <opt. Channel>")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int, channel: discord.TextChannel = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            try:
                if channel is None:
                    channel = ctx.channel
                await channel.edit(slowmode_delay=seconds)
                channelname = channel.name
                embed = discord.Embed(
                    title="**Slowmode**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="⠀",
                    value=f"Der Slowmode vom Channel {channel.mention} wurde zu {seconds} Sekunden geändert.",
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Nutzer "
                    + str(user)
                    + ' hat im Chat "#'
                    + str(channelname)
                    + '" den Slowmode'
                    f" auf {seconds} Sekunden gesetzt.",
                    guildid=ctx.guild.id,
                )
            except Exception:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Bot hatte nicht die nötigen Berrechtigungen um "
                    + await get_prefix_string(ctx.message)
                    + "slowmode auszuführen..",
                    guildid=ctx.guild.id,
                )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(slowmode(bot))
