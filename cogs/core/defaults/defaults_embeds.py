from discord.ext import commands

from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import get_author
from config import FOOTER


class defaults_embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_embed_footer_text(ctx=None, message=None):
    """
    :param message: discord.Message
    :param ctx: commands.Context
    :return: str: footer text
    """
    if ctx:
        footer = (
                FOOTER[0] + str(ctx.author) + FOOTER[1] + str(get_author()) + FOOTER[2]
                + str(get_prefix_string(ctx.message))
        )
    else:
        footer = (
                FOOTER[0] + str(message.author) + FOOTER[1] + str(get_author()) + FOOTER[2]
                + str(get_prefix_string(message))
        )
    return str(footer)


########################################################################################################################


def setup(bot):
    bot.add_cog(defaults_embeds(bot))
