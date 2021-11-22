import asyncio
import datetime
import os
import random
import re
import time as time_lib

import discord
import discord_components
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, ButtonStyle

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_giveaways import (
    create_giveaway,
    add_giveaway_member,
    end_giveaway,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import readjson, writejson
from cogs.core.functions.logging import log
from config import GIVEAWAY

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


async def convert(argument) -> bool and int:
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except Exception:
            return False
    return True and round(time)


async def get_giveaway_embed(
    message, prize, unix_time, winner_amount, author
) -> discord.Embed:
    embed5 = discord.Embed(title="Gewinnspiel", colour=await get_embedcolour(message))
    embed5.add_field(
        name=f"Preis {f'({winner_amount}x)' if winner_amount > 1 else ''}",
        value=prize,
        inline=False,
    )
    embed5.add_field(name="Ende", value=f"<t:{unix_time}:R>", inline=False)
    embed5._footer = await get_embed_footer(
        message=message, replace=[["für", "von"]], author=author
    )
    embed5.set_thumbnail(url=GIVEAWAY)
    return embed5


async def on_giveaway_button(interaction: discord_components.interaction):
    if interaction.component.id == "giveaway_join":
        if await add_giveaway_member(
            message=interaction.message, user=interaction.user
        ):
            await interaction.respond(content="Du nimmst jetzt am Gewinnspiel teil! 🎉")
        else:
            await interaction.respond(content="Du nimmst bereits am Gewinnspiel teil❗")


class giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="giveaway", aliases=["g", "gewinnspiel", "giveaways"])
    @commands.has_permissions(manage_guild=True)
    async def giveaway(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.giveaway_help)

    @giveaway.command(name="help", aliases=["hilfe", "commands"])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_help(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="Giveaway Help",
            description=f"Hier findest du alle Sub-Befehle zu `{prefix}giveaway`",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name=f"{prefix}g help",
            value="Ruft die aktuelle Hilfeseite auf!",
            inline=False,
        )
        embed.add_field(
            name=f"{prefix}g setup", value="Erstelle ein Gewinnspiel!", inline=False
        )
        embed.add_field(
            name=f"{prefix}g end", value="Beende ein Gewinnspiel sofort!", inline=False
        )
        embed.add_field(
            name=f"{prefix}g reroll", value="Verlose ein Gewinnspiel neu!", inline=False
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            "giveaway help benutzt!",
            guildid=ctx.guild.id,
        )

    @giveaway.command(name="setup", aliases=["set"])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_setup(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        embed_timeout = discord.Embed(
            title="TimeOut",
            description="Du hast zu lange für eine Antwort gebraucht, bitte nutze den Befehl erneut!",
            colour=await get_embedcolour(ctx.message),
        )
        embed_timeout._footer = await get_embed_footer(ctx)
        embed_timeout._thumbnail = await get_embed_thumbnail()
        embed1 = discord.Embed(
            title="Giveaway Setup",
            description="Los geht's mit dem Setup! Du kannst den Vorgang jederzeit abbrechen indem du `abbruch` in den Chat schreibst. "
            "In welchem Channel soll das Gewinnspiel stattfinden?",
            colour=await get_embedcolour(ctx.message),
        )
        embed1._footer = await get_embed_footer(ctx)
        embed1._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed1)
        while True:
            try:
                msg: discord.Message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author.id == ctx.author.id
                    and m.channel.id == ctx.channel.id,
                    timeout=60,
                )
            except asyncio.TimeoutError:
                await ctx.send(embed=embed_timeout)
                return
            giveaway_channel = msg.content
            if giveaway_channel == "abbruch":
                await msg.add_reaction(emoji="✅")
                return
            if "<#" in giveaway_channel and ">" in giveaway_channel:
                giveaway_channel = ctx.guild.get_channel(
                    int(giveaway_channel.replace("<#", "").replace(">", ""))
                )
                break
            else:
                channel_check = False
                for guild_channel in ctx.guild.channels:
                    if guild_channel.name == giveaway_channel and isinstance(
                        guild_channel, discord.TextChannel
                    ):
                        giveaway_channel = ctx.guild.get_channel(guild_channel.id)
                        channel_check = True
                        break
                if channel_check:
                    break
            embed1_fehler = discord.Embed(
                title="Giveaway Setup",
                description=f"Ich konnte den Textchannel `{giveaway_channel}` nicht finden! Bitte versuch es erneut!",
                colour=await get_embedcolour(ctx.message),
            )
            embed1_fehler._footer = await get_embed_footer(ctx)
            embed1_fehler._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed1_fehler)
        embed2 = discord.Embed(
            title="Giveaway Setup",
            description=f"Okay, das Gewinnspiel wird in {giveaway_channel.mention} stattfinden. Wie lange soll das Gewinnspiel gehen? "
            f"Bitte hänge dafür `s` für Sekunden, `m` für Minuten, `h` für Stunden und `d` für Tage an! Das könnte z.B. so aussehen:"
            f"```5d 3h 30m 5s (5 Tage / 3 Stunden / 30 Minuten / 5 Sekunden```",
            colour=await get_embedcolour(ctx.message),
        )
        embed2._footer = await get_embed_footer(ctx)
        embed2._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed2)
        while True:
            try:
                msg: discord.Message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author.id == ctx.author.id
                    and m.channel.id == ctx.channel.id,
                    timeout=60,
                )
            except asyncio.TimeoutError:
                await ctx.send(embed=embed_timeout)
                return
            time_raw = msg.content
            if "cancel" in time_raw or "abbruch" in time_raw:
                await msg.add_reaction(emoji="✅")
                return
            if await convert(time_raw):
                giveaway_time = int(time_lib.time()) + await convert(time_raw)
                break
            else:
                embed2_fehler = discord.Embed(
                    title="Giveaway Setup",
                    description=f"Die Zeitangabe {msg.content} ist ungültig! Bitte versuch es erneut!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed2_fehler._footer = await get_embed_footer(ctx)
                embed2_fehler._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed2_fehler)
        embed3 = discord.Embed(
            title="Giveaway Setup",
            description=f"Okay, das Gewinnspiel wird `{time_raw}` dauern! Wie viele Gewinner soll es geben? Bitte gib eine Zahl "
            f"von 1-20 ein!",
            colour=await get_embedcolour(ctx.message),
        )
        embed3._footer = await get_embed_footer(ctx)
        embed3._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed3)
        while True:
            try:
                msg: discord.Message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author.id == ctx.author.id
                    and m.channel.id == ctx.channel.id,
                    timeout=60,
                )
            except asyncio.TimeoutError:
                await ctx.send(embed=embed_timeout)
                return
            if "cancel" in time_raw or "abbruch" in time_raw:
                await msg.add_reaction(emoji="✅")
                return
            try:
                zahl = int(msg.content)
            except ValueError:
                zahl = 1
            if 1 <= zahl <= 20:
                giveaway_winner = int(msg.content)
                break
            else:
                embed3_fehler = discord.Embed(
                    title="Giveaway Setup",
                    description=f"Die Nummer {msg.content} ist ungültig! Bitte versuch es erneut!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed3_fehler._footer = await get_embed_footer(ctx)
                embed3_fehler._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed3_fehler)
        embed4 = discord.Embed(
            title="Giveaway Setup",
            description=f"Okay, es gibt {giveaway_winner} Gewinner! Was willst du verlosen?",
            colour=await get_embedcolour(ctx.message),
        )
        embed4._footer = await get_embed_footer(ctx)
        embed4._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed4)
        try:
            msg: discord.Message = await self.bot.wait_for(
                "message",
                check=lambda m: m.author.id == ctx.author.id
                and m.channel.id == ctx.channel.id,
                timeout=60,
            )
        except asyncio.TimeoutError:
            await ctx.send(embed=embed_timeout)
            return
        giveaway_prize = msg.content
        embed4 = discord.Embed(
            title="Giveaway Setup",
            description=f'Alles klar, möchtest du das Gewinnspiel starten? Dann klick unten einfach auf "Start" oder zum Abbrechen auf "Abbruch"! Mit dem Button'
            f'"Vorschau" kannst du eine Vorschau des Gewinnspiels einsehen!',
            colour=await get_embedcolour(ctx.message),
        )
        embed4._footer = await get_embed_footer(ctx)
        embed4._thumbnail = await get_embed_thumbnail()
        msg = await ctx.send(
            embed=embed4,
            components=[
                [
                    Button(
                        style=ButtonStyle.green,
                        custom_id="giveaway_start",
                        label="Start",
                    ),
                    Button(
                        style=ButtonStyle.red,
                        custom_id="giveaway_cancel",
                        label="Abbruch",
                    ),
                    Button(
                        style=ButtonStyle.blue,
                        custom_id="giveaway_preview",
                        label="Vorschau",
                    ),
                ]
            ],
        )
        while True:
            start_wait = round(time_lib.time())
            try:
                interaction = await self.bot.wait_for(
                    "button_click",
                    check=lambda i: i.message.id == msg.id
                    and i.user.id == ctx.author.id,
                    timeout=60,
                )
                giveaway_time = giveaway_time + (round(time_lib.time()) - start_wait)
            except asyncio.TimeoutError:
                await msg.edit(
                    components=[
                        [
                            Button(
                                style=ButtonStyle.green,
                                custom_id="giveaway_start",
                                label="Start",
                                disabled=True,
                            ),
                            Button(
                                style=ButtonStyle.red,
                                custom_id="giveaway_cancel",
                                label="Abbruch",
                                disabled=True,
                            ),
                            Button(
                                style=ButtonStyle.blue,
                                custom_id="giveaway_preview",
                                label="Vorschau",
                                disabled=True,
                            ),
                        ]
                    ]
                )
                return
            if interaction.component.id == "giveaway_start":
                giveaway_msg = await giveaway_channel.send(
                    embed=await get_giveaway_embed(
                        message=interaction.message,
                        prize=giveaway_prize,
                        unix_time=giveaway_time,
                        winner_amount=giveaway_winner,
                        author=ctx.author,
                    ),
                    components=[
                        Button(
                            style=await get_buttoncolour(message=interaction.message),
                            custom_id="giveaway_join",
                            label="Beitreten",
                            emoji="🎉",
                            disabled=False,
                        )
                    ],
                )
                await create_giveaway(
                    author_id=ctx.author.id,
                    channel_id=giveaway_channel.id,
                    message_id=giveaway_msg.id,
                    unix_time=giveaway_time,
                    winner_amount=giveaway_winner,
                    prize=giveaway_prize,
                    guild=ctx.guild,
                )
                await interaction.respond(
                    content=f"Das Gewinnspiel wurde erfolgreich in {giveaway_channel.mention} gestartet!"
                )
                await msg.edit(
                    components=[
                        [
                            Button(
                                style=ButtonStyle.green,
                                custom_id="giveaway_start",
                                label="Start",
                                disabled=True,
                            ),
                            Button(
                                style=ButtonStyle.red,
                                custom_id="giveaway_cancel",
                                label="Abbruch",
                                disabled=True,
                            ),
                            Button(
                                style=ButtonStyle.blue,
                                custom_id="giveaway_preview",
                                label="Vorschau",
                                disabled=True,
                            ),
                        ]
                    ]
                )
                break
            elif interaction.component.id == "giveaway_cancel":
                await msg.edit(
                    components=[
                        [
                            Button(
                                style=ButtonStyle.green,
                                custom_id="giveaway_start",
                                label="Start",
                                disabled=True,
                            ),
                            Button(
                                style=ButtonStyle.red,
                                custom_id="giveaway_cancel",
                                label="Abbruch",
                                disabled=True,
                            ),
                            Button(
                                style=ButtonStyle.blue,
                                custom_id="giveaway_preview",
                                label="Vorschau",
                                disabled=True,
                            ),
                        ]
                    ]
                )
                await interaction.respond(
                    content="Das Giveaway Setup wurde erfolgreich abgebrochen!"
                )
                return
            elif interaction.component.id == "giveaway_preview":
                embed: discord.Embed = await get_giveaway_embed(
                    message=interaction.message,
                    prize=giveaway_prize,
                    unix_time=giveaway_time,
                    winner_amount=giveaway_winner,
                    author=ctx.author,
                )
                embed.title = "Giveaway Setup"
                await interaction.respond(
                    type=7,
                    embed=embed,
                    components=[
                        [
                            Button(
                                style=ButtonStyle.green,
                                custom_id="giveaway_start",
                                label="Start",
                            ),
                            Button(
                                style=ButtonStyle.red,
                                custom_id="giveaway_cancel",
                                label="Abbruch",
                            ),
                            Button(
                                style=ButtonStyle.blue,
                                custom_id="giveaway_preview",
                                label="Vorschau",
                                disabled=True,
                            ),
                        ]
                    ],
                )
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "giveaway setup benutzt!",
            guildid=ctx.guild.id,
        )

    @giveaway.command(name="end", aliases=["e"])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_end(self, ctx: commands.Context, message_id=None):
        global giveaway_channel
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        giveaway_list = await readjson(
            key="giveaways", path=os.path.join("data", "cache", "giveaway_cache.json")
        )
        if message_id:
            message_id = int(message_id)
        else:
            giveaway_list_reversed = reversed(giveaway_list)
            for giveaway in giveaway_list_reversed:
                if (
                    giveaway["guild_id"] == ctx.guild.id
                    and giveaway["channel_id"] == ctx.channel.id
                ):
                    message_id = giveaway["message_id"]
                    break
        for giveaway in giveaway_list:
            if (
                giveaway["guild_id"] == ctx.guild.id
                and giveaway["message_id"] == message_id
            ):
                giveaway_dict = giveaway
                giveaway_channel = giveaway["channel_id"]
                await end_giveaway(self.bot, giveaway_dict)
                await writejson(
                    key="giveaways",
                    value=giveaway_dict,
                    path=os.path.join("data", "cache", "giveaway_cache.json"),
                    mode="remove",
                )
                break
        else:
            embed = discord.Embed(
                title="Fehler",
                description=f"Es konnte kein aktives Gewinnspiel {'in dem aktuellen Kanal' if not str(message_id) else 'mit der Nachricht-ID'}"
                f" {message_id if message_id else ''} gefunden werden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "giveaway end zu nutzen, es konnte aber kein passendes Gewinnspiel gefunden werden!",
                guildid=ctx.guild.id,
            )
            return
        embed = discord.Embed(
            title="Giveaway End",
            description=f"Das Gewinnspiel mit der Message ID {message_id} wurde erfolgreich beendet!"
            f" \n\n [Jump](https://discord.com/channels/{ctx.guild.id}/{giveaway_channel}/{message_id})",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "giveaway end benutzt!",
            guildid=ctx.guild.id,
        )

    @giveaway.command(name="reroll", aliases=["r"])
    @commands.has_permissions(manage_guild=True)
    async def giveaway_reroll(self, ctx: commands.Context, message_id=None):
        """
        -> findet Nachricht (mid id oder im channel)
        ->
        """
        global giveaway_channel
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        giveaway_list_default = await readjson(
            key="giveaways",
            path=os.path.join("data", "configs", f"{ctx.guild.id}.json"),
        )
        giveaway_list = dict(reversed(list(giveaway_list_default.items())))
        if message_id:
            message_id = int(message_id)
        else:
            for giveaway in giveaway_list:
                giveaway = giveaway_list[str(giveaway)]
                if giveaway["channel_id"] == ctx.channel.id:
                    message_id = giveaway["message_id"]
                    break
        for giveaway in giveaway_list:
            giveaway = giveaway_list[str(giveaway)]
            if giveaway["message_id"] == message_id:
                giveaway_channel = giveaway["channel_id"]
                new_winner = ctx.guild.get_member(random.choice(giveaway["member"]))
                break
        else:
            embed = discord.Embed(
                title="Fehler",
                description=f"Es konnte kein bereits abgelaufenes Gewinnspiel {'in dem aktuellen Kanal' if not str(message_id) else 'mit der Nachricht-ID'}"
                f" {message_id if message_id else ''} gefunden werden, bei dem ein neuer Gewinner ausgelost werden kann!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "giveaway reroll zu nutzen, es konnte aber kein passendes Gewinnspiel gefunden werden!",
                guildid=ctx.guild.id,
            )
            return
        embed = discord.Embed(
            title="Giveaway Reroll",
            description=f"Beim Gewinnspiel mit der Message ID {message_id} wurde {new_winner.mention} als neuer Gewinner ausgelost!"
            f" \n\n [Jump](https://discord.com/channels/{ctx.guild.id}/{giveaway_channel}/{message_id})",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "giveaway reroll benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(giveaways(bot))
