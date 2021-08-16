import re

from discord.ext import commands

from config import BOT_MAIN_DEVELOPER, BOT_NAME


class functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_author():
    return str(BOT_MAIN_DEVELOPER)


def get_botname():
    return str(BOT_NAME)


def is_not_pinned(message):
    return not message.pinned


def whoisr(member):
    if member.bot is True:
        return str("Ja")
    return str("Nein")


def msg_contains_word(msg, word):
    return re.search(fr"\b({word})\b", msg) is not None


########################################################################################################################


def setup(bot):
    bot.add_cog(functions(bot))
