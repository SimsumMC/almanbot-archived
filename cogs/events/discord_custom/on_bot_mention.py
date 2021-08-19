import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log
from config import THUMBNAIL_URL, FOOTER, ICON_URL


class on_bot_mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_bot_mention(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        embed = discord.Embed(title="**Prefix**", color=get_embedcolour(message))
        embed.set_footer(
            text=FOOTER[0]
                 + message.author.name
                 + FOOTER[1]
                 + str(get_author())
                 + FOOTER[2]
                 + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=" ⠀ ",
            value=f"Mein Prefix hier ist: ```{get_prefix_string(message)}```",
            inline=True,
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        await message.channel.send(embed=embed)
        log(
            f"{time}: Der Spieler {user} hat sich den Prefix über eine Erwähnung ausgeben lassen.",
            message.guild.id,
        )

########################################################################################################################


def setup(bot):
    bot.add_cog(on_bot_mention(bot))
