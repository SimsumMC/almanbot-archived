import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class on_bot_mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_bot_mention(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        embed = discord.Embed(title="**Prefix**", color=await get_embedcolour(message))
        embed.add_field(
            name=" ⠀ ",
            value=f"Mein Prefix hier ist: ```{await get_prefix_string(message)}```",
            inline=True,
        )
        embed._footer, embed._thumbnail = (
            await get_embed_footer(message=message),
            await get_embed_thumbnail(),
        )
        await message.channel.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat sich den Prefix über eine Erwähnung ausgeben lassen.",
            message.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_bot_mention(bot))
