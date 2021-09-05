import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER


class servericon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["serverbild", "serveravatar"])
    async def servericon(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            embed = discord.Embed(
                title=f"**Servericon von {ctx.guild.name}**",
                colour=get_embedcolour(ctx.message),
            )
            embed.set_image(url=ctx.guild.icon_url)
            embed._footer = get_embed_footer(ctx)
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "servericon benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(servericon(bot))
