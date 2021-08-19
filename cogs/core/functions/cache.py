from discord.ext import commands


class cache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


embed_cache = {}

author_message_cache = {}


async def save_embed_to_cache(embed, messageid):
    embed_cache[str(messageid)] = {
        "title": str(embed.title),
        "description": str(embed.description)
    }


async def get_embed_from_cache(messageid):
    return embed_cache[str(messageid)]


async def save_message_to_cache(message):
    if not author_message_cache[str(message.author.id)]:
        author_message_cache[str(message.author.id)] = []
    author_message_cache[str(message.author.id)] = author_message_cache[str(message.author.id)].append[message.id]


async def get_messages_from_cache(authorid):
    return author_message_cache[str(authorid)]


########################################################################################################################


def setup(bot):
    bot.add_cog(cache(bot))
