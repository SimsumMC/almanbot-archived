import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


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
            "kontaktiere einen Moderator des "
            "Servers. ",
            colour=get_embedcolour(message=message),
        )
        embed._footer = get_embed_footer(message=message)
        embed._thumbnail = get_embed_thumbnail()
        await message.channel.send(embed=embed, delete_after=5)
        log(
            f"{time}: Der Nutzer {user} hat versucht ein verbotenes Wort zu benutzen."
            f' Wort: "{bannedword}"',
            message.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_blacklist_word(bot))
