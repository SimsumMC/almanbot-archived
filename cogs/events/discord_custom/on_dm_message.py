import discord
from discord.ext import commands

from cogs.core.functions.functions import (
    get_author,
)
from config import THUMBNAIL_URL, FOOTER, ICON_URL, DEFAULT_PREFIX


class on_dm_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_dm_message(self, message):
        embed = discord.Embed(title="Hinweis | Note", colour=0xF00000)
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.add_field(
            name="German",
            value="Dieser Bot hat keine DM Funktion - daher bringt es nichts "
            "mich hier zu kontaktieren.",
            inline=False,
        )
        embed.add_field(
            name="English",
            value="This bot don't have a DM Function - so you cant achieve something "
            "with writing something to me.",
            inline=False,
        )
        embed.set_footer(
            text=f"{FOOTER[0]}{message.author.name}{FOOTER[1]}{str(get_author())}{FOOTER[2]}{DEFAULT_PREFIX}",
            icon_url=ICON_URL,
        )
        await message.channel.send(embed=embed)
        return


########################################################################################################################


def setup(bot):
    bot.add_cog(on_dm_message(bot))
