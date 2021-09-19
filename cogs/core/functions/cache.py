import json
import os
import traceback
from discord.ext import commands


class cache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


embed_cache = {}


async def save_embed_to_cache(embed, messageid):
    embed_cache[str(messageid)] = {
        "title": str(embed.title),
        "description": str(embed.description),
        "thumbnail": str(embed.thumbnail),
        "footer": str(embed.footer),
    }


async def get_embed_from_cache(messageid):
    return embed_cache[str(messageid)]


async def save_message_to_cache(message, author, max_uses: int = None):
    path = os.path.join("data", "cache", "message_cache.json")
    with open(path, "r") as f:
        message_cache = json.load(f)
    try:
        if str(author.id) not in message_cache:
            message_cache[str(author.id)] = [message.id]
        else:
            message_cache[str(author.id)].append(message.id)
        with open(path, "w") as f:
            json.dump(message_cache, f, indent=4)
    except Exception:
        traceback.print_exc()


async def get_messages_from_cache(authorid):
    path = os.path.join("data", "cache", "message_cache.json")
    with open(path, "r") as f:
        message_cache = json.load(f)
    if str(authorid) not in message_cache:
        return []
    return message_cache[str(authorid)]


########################################################################################################################


def setup(bot):
    bot.add_cog(cache(bot))
