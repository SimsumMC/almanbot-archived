import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_trigger import get_trigger_msg
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log
from config import THUMBNAIL_URL


class on_trigger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_trigger(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        answer = get_trigger_msg(guildid=message.guild.id, trigger=message.content)
        if answer is not None:
            embed = discord.Embed(
                title="**Trigger**",
                description=answer,
                color=get_embedcolour(message),
            )
            embed.set_footer(
                text="for "
                     + str(user)
                     + " | by "
                     + str(get_author())
                     + " | Prefix "
                     + str(get_prefix_string(message)),
                icon_url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739"
                         "/winging-easy.png?width=676&height=676",
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            await message.channel.send(embed=embed)
            log(f'{time}: Der Nutzer {user} hat den Trigger "{message.content}" aufgerufen.', id=message.guild.id)

########################################################################################################################


def setup(bot):
    bot.add_cog(on_trigger(bot))
