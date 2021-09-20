import discord
from discord.ext import commands

from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from config import DEFAULT_EMBEDCOLOUR


class on_dm_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_dm_message(self, message):
        embed = discord.Embed(title="Hinweis | Note", colour=DEFAULT_EMBEDCOLOUR)
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
        embed._footer, embed._thumbnail = (
            await get_embed_footer(message=message, dm=True),
            await get_embed_thumbnail(),
        )
        await message.channel.send(embed=embed)
        return


########################################################################################################################


def setup(bot):
    bot.add_cog(on_dm_message(bot))
