import json
import os
import random

import discord
from discord.ext import commands
from discord_components import Button
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import writejson
from config import GIVEAWAY


class config_general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # giveaway Config things


async def end_giveaway(client: discord.Client, giveaway: dict):
    try:
        from cogs.commands.Tools.giveaways import get_giveaway_embed

        guild: discord.Guild = client.get_guild(int(giveaway["guild_id"]))
        channel: discord.TextChannel = guild.get_channel(int(giveaway["channel_id"]))
        message: discord.Message = await channel.fetch_message(giveaway["message_id"])

        # Set Active to False in Guild Config and get Member of Giveaway

        path = os.path.join("data", "configs", f"{guild.id}.json")
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)
        data["giveaways"][str(message.id)]["active"] = False
        member: list = data["giveaways"][str(message.id)]["member"]
        with open(path, "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)

        # Edit Message & Notify Winner

        x, winner, cache_member = 0, [], member[:]
        if member:
            winner_amount = (
                giveaway["winner_amount"]
                if len(member) >= giveaway["winner_amount"]
                else len(member)
            )
            while x < winner_amount:
                while True:
                    cache_winner: discord.Member = guild.get_member(
                        int(random.choice(cache_member))
                    )
                    if cache_winner:
                        winner.append(cache_winner)
                        cache_member.remove(cache_winner.id)
                        break
                x += 1
            channel_embed = discord.Embed(
                title="Herzlichen Glückwunsch 🎉",
                colour=await get_embedcolour(message=message),
                description="Wenn du in der Nachricht erwähnt wurdest, gehörst du zu den glücklichen Gewinnern!",
            )
            channel_embed.add_field(name="Preis", value=giveaway["prize"], inline=False)
            channel_embed.add_field(
                name="Teilnehmer", value=str(len(member)), inline=False
            )
            channel_embed.set_thumbnail(url=GIVEAWAY)
            channel_embed._footer = await get_embed_footer(
                message=message, replace=[["für", "von"]]
            )
            await channel.send(
                content="".join([str(w.mention) + " " for w in winner]),
                embed=channel_embed,
            )
        embed: discord.Embed = await get_giveaway_embed(
            message=message,
            prize=giveaway["prize"],
            unix_time=giveaway["unix_time"],
            winner_amount=giveaway["winner_amount"],
            author=guild.get_member(giveaway["author_id"]),
        )
        embed.add_field(
            name="Gewinner",
            value="".join(
                [str(w.mention) + ", " for w in winner]
                if winner
                else "Es konnte kein Gewinner ausgewählt werden da niemand teilgenommen hat!"
            )[:-2],
        )
        await message.edit(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(message=message),
                    label="Beendet",
                    emoji="💥",
                    disabled=True,
                )
            ],
        )
    except Exception:
        embed = discord.Embed(
            title="Fehler",
            description="Das Gewinnspiel das nun enden sollte konnte nicht beendet werden! Sicher das der Channel nicht gelöscht wurde? ",
            colour=await get_embedcolour(guild),
        )
        embed._footer = await get_embed_footer(guild=guild, author=guild.owner)
        embed._thumbnail = await get_embed_thumbnail()
        await guild.owner.send(embed=embed)


async def create_giveaway(
    message_id,
    author_id,
    channel_id,
    winner_amount,
    prize,
    unix_time,
    guild: discord.Guild,
):
    path = os.path.join("data", "configs", f"{guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if "giveaways" not in data:
        data["giveaways"] = {}
    giveaway_dict = {
        "message_id": message_id,
        "channel_id": channel_id,
        "unix_time": unix_time,
        "winner_amount": winner_amount,
        "author_id": author_id,
        "prize": prize,
        "active": True,
        "member": [],
    }
    data["giveaways"][str(message_id)] = giveaway_dict
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)
    giveaway_dict["guild_id"] = guild.id
    del giveaway_dict["member"]
    del giveaway_dict["active"]
    await writejson(
        key="giveaways",
        value=giveaway_dict,
        mode="append",
        path=os.path.join("data", "cache", "giveaway_cache.json"),
    )


async def add_giveaway_member(message: discord.Message, user: discord.Member):
    path = os.path.join("data", "configs", f"{message.guild.id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    if user.id not in data["giveaways"][str(message.id)]["member"]:
        data["giveaways"][str(message.id)]["member"].append(user.id)
        with open(path, "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)
        return True
    return False


########################################################################################################################


def setup(bot):
    bot.add_cog(config_general(bot))
