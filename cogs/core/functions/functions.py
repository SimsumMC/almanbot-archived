import re

from discord.ext import commands

from config import BOT_MAIN_DEVELOPER, BOT_NAME


class functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def get_author():
    return str(BOT_MAIN_DEVELOPER)


async def get_botname():
    return str(BOT_NAME)


def is_not_pinned(message):
    return not message.pinned


async def whoisr(member):
    if member.bot is True:
        return str("Ja")
    return str("Nein")


async def msg_contains_word(msg, word):
    return re.search(fr"\b({word})\b", msg) is not None


########################################################################################################################


def setup(bot):
    bot.add_cog(functions(bot))
