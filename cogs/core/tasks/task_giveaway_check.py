import asyncio
import json
import os
import time
import discord
import random
from discord.ext import commands, tasks
from discord_components import Button

from cogs.commands.Tools.giveaways import get_giveaway_embed
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.func_json import readjson, writejson
from config import GIVEAWAY


class giveaway_check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_ended_giveaways.start()

    async def end_giveaway(self, giveaway: dict):
        guild: discord.Guild = self.bot.get_guild(int(giveaway["guild_id"]))
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
        print(member)
        # Edit Message & Notify Winner
        x, winner, cache_member = 0, [], member
        if member:
            winner_amount = giveaway["winner_amount"] if len(member) >= giveaway["winner_amount"] else len(member)
            while x < winner_amount:
                while True:
                    cache_winner: discord.Member = guild.get_member(int(random.choice(cache_member)))
                    if cache_winner:
                        winner.append(cache_winner)
                        cache_member.remove(cache_winner.id)
                        break
                x += 1
            channel_embed = discord.Embed(title="Herzlichen Glückwunsch 🎉", colour=await get_embedcolour(message=message),
                                          description="Wenn du in der Nachricht erwähnt wurdest, gehörst du zu den Gewinnern!")
            channel_embed.add_field(name="Preis", value=giveaway["prize"])
            print(member)
            channel_embed.add_field(name="Teilnehmer", value=str(len(member)))
            channel_embed.set_thumbnail(url=GIVEAWAY)
            channel_embed._footer = await get_embed_footer(message=message, replace=[["für", "von"]])
            await channel.send(content="".join([str(w.mention) + " " for w in winner]), embed=channel_embed)
        embed: discord.Embed = await get_giveaway_embed(message=message, prize=giveaway["prize"],
                                                        unix_time=giveaway["unix_time"],
                                                        winner_amount=giveaway["winner_amount"],
                                                        author=guild.get_member(giveaway["author_id"]))
        embed.add_field(name="Gewinner", value="".join([str(w.mention) + ", " for w in
                                                        winner] if winner else "Es konnte kein Gewinner ausgewählt werden da keiner am Gewinnspiel teilgenommen hat!")[
                                               :-2])
        await message.edit(embed=embed,
                           components=[
                               Button(style=await get_buttoncolour(message=message), label="Beendet", emoji="💥",
                                      disabled=True)])

    @tasks.loop(seconds=5)
    async def check_for_ended_giveaways(self):
        await self.bot.wait_until_ready()
        print("loop")
        path = os.path.join("data", "cache", "giveaway_cache.json")
        actual_time = round(time.time())
        print(actual_time)
        data = await readjson(key="giveaways", path=path)
        item, remove = 0, []
        for giveaway in data:
            print(giveaway)
            if giveaway["unix_time"] <= actual_time:
                "passed"
                await self.end_giveaway(giveaway)
                remove.append(giveaway)
            item += 1
        # get Actual data & remove Giveaways
        data: list = await readjson(key="giveaways", path=path)
        for item in remove:
            try:
                data.remove(item)
            except ValueError:
                pass
        await writejson(key="giveaways", value=data, path=path)


def setup(bot):
    bot.add_cog(giveaway_check(bot))
