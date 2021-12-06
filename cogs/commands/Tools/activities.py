import asyncio
import datetime

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Select, SelectOption, ComponentMessage

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log
from config import DISCORD_TOKEN


async def convert_gamename_id(name: str) -> int:
    game_ids = {
        "betrayal": 773336526917861400,
        "chess": 832012586023256104,
        "doodle_crew": 878067389634314250,
        "fishing": 814288819477020702,
        "letter_tile": 879863686565621790,
        "poker": 755827207812677713,
        "spell_cast": 852509694341283871,
        "word_snack": 879863976006127627,
        "youtube": 755600276941176913,
    }
    return game_ids[name]


async def get_activity_invite(ctx: commands.Context, activity_id) -> str:
    url = f"https://discord.com/api/v9/channels/{ctx.author.voice.channel.id}/invites"
    api_json = {
        "max_age": 604800,
        "max_uses": 0,
        "uses": 1,
        "target_application_id": activity_id,
        "target_type": 2,
        "temporary": False,
        "unique": True,
        "validate": None,
    }
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.request(
                "POST", url, headers=headers, json=api_json
        ) as response:
            data = await response.json()
            return "https://discord.com/invite/" + data["code"]


class activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="party", aliases=["aktivitäten", "games", "spiele", "activities"]
    )
    async def party(self, ctx: commands.Context, game_id=None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler",
                description="Du befindest dich in keinem Sprachkanal!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "activities zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        if not game_id:
            embed = discord.Embed(
                title="Activities",
                description="Wähle unten ganz einfach über das Auswahlfenster eine Aktivität aus!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            msg = await ctx.send(
                embed=embed,
                components=[
                    Select(
                        placeholder="Aktivität Auswählen",
                        options=[
                            SelectOption(label="YouTube WatchTogether", value="youtube", emoji="🎥"),
                            SelectOption(label="Schach", value="chess", emoji="♟"),
                            SelectOption(label="Poker", value="poker", emoji="🃏"),
                            SelectOption(label="Fishington", value="fishing", emoji="🎣"),
                            SelectOption(label="Betrayal", value="betrayal", emoji="🔪"),
                            SelectOption(label="Doodle Crew", value="doodle_crew", emoji="🖍"),
                            SelectOption(label="Scrabble", value="letter_tile", emoji="🎓"),
                            SelectOption(label="Spell Cast", value="spell_cast", emoji="📱"),
                            SelectOption(label="Word Snack", value="word_snack", emoji="☕"),
                        ],
                        custom_id="activities_choose",
                    )
                ],
            )
            try:
                interaction = await self.bot.wait_for(
                    event="select_option",
                    timeout=15.0,
                    check=lambda inter: inter.custom_id == "activities_choose"
                                        and inter.message.id == msg.id
                                        and inter.author.id == ctx.author.id,
                )
                try:
                    embed.add_field(
                        name="Link",
                        value=await get_activity_invite(
                            ctx, await convert_gamename_id(interaction.values[0])
                        ),
                    )
                    await interaction.respond(type=7, embed=embed)
                except Exception:
                    interaction.respond(
                        f"Beim erstellen des Invite-Links ist ein Fehler aufgetreten!"
                    )
                await log(
                    f"{time}: Der Nutzer {user} hat mit dem Select des Activitys-Befehl interagiert!",
                    ctx.guild.id,
                )
            except asyncio.TimeoutError:
                pass
            await msg.disable_components()
            return
        else:
            try:
                embed = discord.Embed(
                    title="Activities",
                    description=f"Klicke auf den folgenden Link, um die Aktivität zu starten:\n{await get_activity_invite(ctx, game_id)}",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
            except Exception:
                embed = discord.Embed(
                    title="Fehler",
                    description=f"Die Aktivität mit der ID `{game_id}` konnte nicht gefunden werden!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    text=f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}activities zu nutzen, gab jedoch eine ungültige ID an!",
                    guildid=ctx.guild.id,
                )
                return
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "activities benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(activities(bot))
