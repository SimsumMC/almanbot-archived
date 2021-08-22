import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from config import ICON_URL, FOOTER
from cogs.core.functions.functions import get_author
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from main import client


class channelclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channelclear(self, ctx):
        channelid = ctx.channel.id
        channel1 = client.get_channel(channelid)
        time = datetime.datetime.now()
        user = ctx.author.name
        await channel1.clone()
        await channel1.delete()
        log(
            text=str(time)
            + ": Der Spieler "
            + str(user)
            + ' hat den Chat "#'
            + str(channel1)
            + '" gecleart.',
            guildid=ctx.guild.id,
        )

    @channelclear.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(message=ctx.message)
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
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um "
                + get_prefix_string(ctx.message)
                + "channelclear zu nutzen.",
                guildid=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(channelclear(bot))
