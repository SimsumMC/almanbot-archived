import datetime
import os

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.func_json import readjson
from cogs.core.functions.functions import (
    get_author, msg_contains_word,
)
from cogs.core.functions.logging import log
from config import FOOTER, ICON_URL, TESTING_MODE, BLACKLIST_IGNORE


class on_blacklist_check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_blacklist_check(self, message):
        time = datetime.datetime.now()
        user = message.author.name
        path = os.path.join("data", "configs", f"{message.guild.id}.json")
        bannedWords = readjson(type="blacklist", path=path)
        if bannedWords:
            if TESTING_MODE is not True:
                if message.author.id == message.guild.owner_id:
                    return
            for bannedWord in bannedWords:
                if msg_contains_word(message.content.lower(), bannedWord):
                    for ignorearg in BLACKLIST_IGNORE:
                        if msg_contains_word(message.content.lower(), ignorearg):
                            return
                    else:
                        await message.delete()
                        embed = discord.Embed(
                            title="**Fehler**",
                            description="Deine Nachricht hat ein verbotenes Wort "
                            "enthalten, daher wurde sie gelöscht. "
                            "Sollte dies ein Fehler sein "
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
                            + f": Der Spieler {user} hat versucht ein verbotenes Wort zu benutzen."
                            ' Wort: "{bannedWord}"',
                            message.guild.id,
                        )
                        return

########################################################################################################################


def setup(bot):
    bot.add_cog(on_blacklist_check(bot))
