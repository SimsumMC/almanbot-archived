import datetime
import os

import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import get_botchannel
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_memechannel import get_memechannel
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.func_json import writejson
from cogs.core.functions.logging import log


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
        if channel.id in await get_botchannel(message=channel):
            await writejson(
                key="botchannel",
                value=newchannel.id,
                path=os.path.join("data", "configs", f"{channel.guild.id}.json"),
                mode="append",
            )
        elif channel.id in await get_memechannel(message=channel):
            await writejson(
                key="memechannel",
                value=newchannel.id,
                path=os.path.join("data", "configs", f"{channel.guild.id}.json"),
                mode="append",
            )
        await channel.delete()
        embed = discord.Embed(
            title="**Channelclear**",
            description=f"Der Channel {newchannel.mention} wurde erfolgreich geleert!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await newchannel.send(embed=embed)
        await log(
            text=str(time)
            + ": Der Nutzer "
            + str(user)
            + ' hat den Channel "#'
            + str(channel)
            + '" geleert.',
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(channelclear(bot))
