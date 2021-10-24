from discord.ext import commands
import discord
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import get_author
from config import FOOTER, ICON_URL, THUMBNAIL_URL, DEFAULT_PREFIX


class defaults_embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_embed_footer(
    ctx: commands.Context = None,
    author: discord.Member = None,
    message: discord.Message = None,
    dm: bool = False,
    guild: discord.Guild = None,
    replace: list = None,
) -> dict:
    """
    :param ctx: discord.ext.commands.Context -> author / prefix
    :param message: discord.Message -> author / prefix
    :param guild: discord.Guild -> prefix
    :param dm: bool -> prefix
    :param author: discord.Member -> author
    :param replace: list of arrays, for example [["1", "2"]] would replace "1" in the footer with "2"
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
            + str(
                await get_prefix_string(message=message, guild=guild)
                if not dm
                else DEFAULT_PREFIX
            )
        ),
        "icon_url": ICON_URL,
    }
    if replace:
        for rep in replace:
            footer_dict["text"] = footer_dict["text"].replace(rep[0], rep[1])
    return footer_dict


async def get_embed_thumbnail() -> dict:
    return {"url": THUMBNAIL_URL}


########################################################################################################################


def setup(bot):
    bot.add_cog(defaults_embeds(bot))
