import datetime

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log


class on_command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg = ctx.message.content
        msg2 = ctx.message
        name = ctx.channel.name
        if isinstance(error, CommandNotFound):
            return
            # out of function for verifying on top.gg
            if botchannel_check(ctx):
                embed = discord.Embed(
                    title="Fehler",
                    description='Der Befehl "' + str(msg) + '" existiert nicht!',
                    color=get_embedcolour(ctx.message),
                )
                embed.set_footer(
                    text="for "
                    + str(user)
                    + " | by "
                    + str(get_author())
                    + " | Prefix "
                    + get_prefix_string(message=ctx.message),
                    icon_url="https://media.discordapp.net/attachments/645276319311200286"
                    "/803322491480178739"
                    "/winging-easy.png?width=676&height=676",
                )
                await ctx.send(embed=embed)
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat probiert den ungültigen Befehl "'
                    + str(msg)
                    + '" zu nutzen!',
                    id=ctx.guild.id,
                )
            else:
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat probiert den ungültigen Befehl "'
                    + str(msg)
                    + '" zu nutzen!',
                    id=ctx.guild.id,
                )
                await ctx.send(
                    str(mention)
                    + ", dieser Befehl kann nur im Kanal #{} genutzt werden.".format(
                        channel
                    ),
                    delete_after=3,
                )
                await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(on_command_error(bot))
