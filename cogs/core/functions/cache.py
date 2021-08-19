import traceback

from discord.ext import commands


class cache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


embed_cache = {}

message_cache = {}


async def save_embed_to_cache(embed, messageid):
    embed_cache[str(messageid)] = {
        "title": str(embed.title),
        "description": str(embed.description)
    }


async def get_embed_from_cache(messageid):
    return embed_cache[str(messageid)]


async def save_message_to_cache(message):  # todo
    try:
        if str(message.author.id) not in message_cache:
            message_cache[str(message.author.id)] = []
        message_cache[str(message.author.id)].append(message.id)
    except Exception:
        traceback.print_exc()


def get_messages_from_cache(authorid):  # todo
    if str(authorid) not in message_cache:
        return []
    return message_cache[str(authorid)]


########################################################################################################################


def setup(bot):
    bot.add_cog(cache(bot))
