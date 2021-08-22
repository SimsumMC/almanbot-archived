import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR


class servericon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["serverbild", "serveravatar"])
    async def servericon(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            embed = discord.Embed(
                title=f"**Servericon von {ctx.guild.name}**",
                colour=get_embedcolour(ctx.message),
            )
            embed.set_image(url=ctx.guild.icon_url)
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
            log(
                f"{time}: Der Spieler {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "servericon benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            log(
                text=f"{time}: Der Spieler {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                f"servericon im Channel #{name} zu benutzen!",
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


########################################################################################################################


def setup(bot):
    bot.add_cog(servericon(bot))
