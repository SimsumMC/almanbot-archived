import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class ssp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ssp(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Schere Stein Papier**",
                description='Lass uns "Schere Stein Papier" spielen!'
                "Nutze dazu die Commands:",
                colour=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            embed.add_field(
                name=get_prefix_string(ctx.message) + "schere",
                value="Spiele die Schere aus!",
                inline=False,
            )
            embed.add_field(
                name=get_prefix_string(ctx.message) + "stein",
                value="Spiele den Stein aus!",
                inline=False,
            )
            embed.add_field(
                name=get_prefix_string(ctx.message) + "papier",
                value="Spiele das Papier aus!",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "ssp benutzt!",
                guildid=ctx.guild.id,
            )

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(ssp(bot))
