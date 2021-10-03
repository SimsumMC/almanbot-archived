from discord.ext import commands

from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import get_author
from config import FOOTER, ICON_URL, THUMBNAIL_URL, DEFAULT_PREFIX


class defaults_embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_embed_footer(ctx=None, author=None, message=None, dm=False, guild=None) -> dict:
    """
    :param dm:
    :param author:
    :param ctx:
    :param message:
    :return: dictionary
    """
    if ctx:
        message = ctx.message
    if not author:
        author = message.author
    footer_dict = {
        "text": (
            FOOTER[0]
            + str(author)
            + FOOTER[1]
            + str(await get_author())
            + FOOTER[2]
            + str(await get_prefix_string(message=message, guild=guild) if not dm else DEFAULT_PREFIX)
        ),
        "icon_url": ICON_URL,
    }
    return footer_dict


async def get_embed_thumbnail() -> dict:
    return {"url": THUMBNAIL_URL}


########################################################################################################################


def setup(bot):
    bot.add_cog(defaults_embeds(bot))
