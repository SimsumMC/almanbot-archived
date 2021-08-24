import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import get_author
from cogs.core.functions.logging import log
from config import FOOTER, ICON_URL


class broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="broadcast", aliases=["ankündigung", "ownermsg"])
    async def broadcast(self, ctx, *, message):
        user = ctx.author
        name = ctx.channel.name
        msg2 = ctx.message
        time = datetime.datetime.now()
        if botchannel_check(ctx):
            ...
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
                text=str(time)
                      + ": Der Spieler "
                      + str(user)
                      + ' hat sich probiert den noch nicht existierenden Log mit der ID "'
                      + str(ctx.guild.id)
                      + '" ausgeben zu lassen!',
                guildid=ctx.guild.id,
            )


###############################################################################################################

def setup(bot):
    bot.add_cog(broadcast(bot))