import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_trigger import get_trigger_msg
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class on_trigger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_trigger(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        answer = await get_trigger_msg(
            guildid=message.guild.id, trigger=message.content
        )
        if answer is not None:
            embed = discord.Embed(
                title="**Trigger**",
                description=answer,
                color=await get_embedcolour(message),
            )
            embed._footer, embed._thumbnail = (
                await get_embed_footer(message=message),
                await get_embed_thumbnail(),
            )
            await message.channel.send(embed=embed)
            await log(
                f'{time}: Der Nutzer {user} hat den Trigger "{message.content}" aufgerufen.',
                guildid=message.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_trigger(bot))
