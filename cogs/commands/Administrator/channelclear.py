import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL
from main import client


class channelclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="channelclear", usage="<opt. Channel>")
    @commands.has_permissions(administrator=True)
    async def channelclear(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        time = datetime.datetime.now()
        user = ctx.author.name
        newchannel = await channel.clone()
        await channel.delete()
        embed = discord.Embed(title="**Channelclear**", description=f"Der Channel {newchannel.mention} wurde erfolgreich geleert!",
                              colour=get_embedcolour(ctx.message))
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_footer(text=get_embed_footer_text(ctx), icon_url=ICON_URL)
        await newchannel.send(embed=embed)
        log(
            text=str(time)
            + ": Der Nutzer "
            + str(user)
            + ' hat den Chat "#'
            + str(channel)
            + '" geleert.',
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(channelclear(bot))
