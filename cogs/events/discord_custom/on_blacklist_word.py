import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log
from config import FOOTER, ICON_URL


class on_blacklist_word(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_blacklist_word(self, message, bannedword):
        time = datetime.datetime.now()
        user = message.author.name
        await message.delete()
        embed = discord.Embed(
            title="**Fehler**",
            description="Deine Nachricht hat ein verbotenes Wort "
            "enthalten, daher wurde sie gelöscht. "
            "Sollte dies ein Fehler sein, "
            "kontaktiere einen Administrator des "
            "Servers. ",
            colour=get_embedcolour(message=message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + message.author.name
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        await message.channel.send(embed=embed, delete_after=5)
        log(
            str(time)
            + f": Der Nutzer {user} hat versucht ein verbotenes Wort zu benutzen."
            f' Wort: "{bannedword}"',
            message.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_blacklist_word(bot))
