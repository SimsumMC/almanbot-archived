import asyncio
import datetime
import inspect
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot, MissingRequiredArgument
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_trigger import (
    get_trigger_list,
    add_trigger,
    remove_trigger,
    get_trigger_msg,
)
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import readjson, writejson
from cogs.core.functions.logging import log
from config import DEFAULT_TRIGGER_LIST, DEFAULT_TRIGGER


class trigger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def trigger(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.help)

    @trigger.command(name="help", aliases=["hilfe"])
    @commands.has_permissions(administrator=True)
    async def help(self, ctx):
        if not await botchannel_check(ctx=ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        embed = discord.Embed(
            title="**Trigger Hilfe**",
            description=f"Hier findest du alle Subbefehle zum {prefix}trigger Befehl!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name=f"**{prefix}trigger hilfe**",
            value=f"Hier siehst du alle Subbefehle zum {prefix}trigger Befehl!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}trigger list**",
            value="Zeigt alle konfigurierten Trigger an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}trigger add <Name : Wert>**",
            value="Füge einen Trigger hinzu!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}trigger remove <Name>**",
            value="Lösche einen bestimmten Trigger!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}trigger edit <Name : Wert>**",
            value="Bearbeite einen Trigger!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}trigger reset**",
            value="Löscht alle konfigurierten Trigger an!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            text=str(time)
            + ": Der Nutzer "
            + str(user)
            + " hat den Befehl "
            + prefix
            + "trigger hilfe benutzt.",
            guildid=ctx.guild.id,
        )

    @trigger.command(name="list", aliases=["liste", "show", "all"])
    async def list(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        trigger_list: list = dict(await readjson(key="trigger", path=path))[
            "triggerlist"
        ]
        embed = discord.Embed(
            title="**Trigger List**",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name="‎",
            value="".join([trigger_name + ", " for trigger_name in trigger_list])[:-2]
            if trigger_list != []
            else "Keine Wörter vorhanden",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat sich mit dem Befehl {await get_prefix_string(ctx.message)}trigger list die Triggerlist ausgeben lassen!",
            guildid=ctx.guild.id,
        )

    @trigger.command(name="reset", aliases=["zurücksetzen", "delall"])
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx: commands.Context):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        trigger_list: list = dict(await readjson(key="trigger", path=path))[
            "triggerlist"
        ]
        trigger_dict: dict = await readjson(key="trigger", path=path)
        default_trigger_dict = {
            "triggerlist": DEFAULT_TRIGGER_LIST,
            "triggermsg": DEFAULT_TRIGGER,
        }
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        elif not trigger_list:
            embed = discord.Embed(
                title="**Fehler**",
                description="Es existieren keine Trigger die gelöscht werden können!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}trigger reset alle Trigger zu löschen, es existierten aber keine!",
                guildid=ctx.guild.id,
            )
            return
        await writejson(key="trigger", value=default_trigger_dict, path=path)
        embed = discord.Embed(
            title="**Trigger Reset**",
            description="Alle Trigger wurden erfolgreich gelöscht!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        msg = await ctx.send(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(ctx.message),
                    label="Wiederherstellung",
                    custom_id="restore-trigger",
                )
            ],
        )
        try:
            res = await self.bot.wait_for(
                event="button_click",
                timeout=15.0,
                check=lambda inter: inter.custom_id == "restore-trigger"
                and inter.message.id == msg.id
                and inter.author.id == ctx.author.id,
            )
            await writejson(key="trigger", value=trigger_dict, path=path)
            await res.respond(
                content="Die Trigger wurden erfolgreich wiederhergestellt!"
            )
            await log(
                f'{time}: Der Nutzer {user} hat mit dem Button "Wiederherstellung" die Trigger nach dem Löschvorgang wiederhergestellt!',
                ctx.guild.id,
            )
        except asyncio.TimeoutError:
            pass
        await msg.edit(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(ctx.message),
                    label="Wiederherstellung",
                    disabled=True,
                )
            ],
        )

    @trigger.command(name="add", usage="<Trigger Name : Antwort Nachricht>")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: commands.Context, *, content):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx=ctx):
            try:
                word = content.split(" : ")[0]
                msg = content.split(" : ")[1]
            except Exception:

                class error(inspect.Parameter):
                    name = "trigger add"
                    param = "subcommand"

                raise MissingRequiredArgument(error)
            if word in await get_trigger_list(guildid=ctx.guild.id):
                embed = discord.Embed(
                    title=f"**Fehler**",
                    description=f"Der Trigger {word} existiert bereits! Wenn du ihn verändern möchtest, "
                    f"nutze den Befehl:"
                    f"```{await get_prefix_string(message=ctx.message)}trigger edit```",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                    f"trigger add zu benutzen und damit den Trigger {word} hinzuzufügen, konnte"
                    f" es aber nicht da dieser bereits existiert hat!",
                    guildid=ctx.guild.id,
                )
                return
            await add_trigger(guildid=ctx.guild.id, trigger=word, msg=msg)
            embed = discord.Embed(
                title=f"**Trigger Add**",
                description=f"Der Bot reagiert nun auf ```{word}``` mit der Nachricht:"
                f"```{msg}```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                f"trigger add benutzt und damit den Trigger {word} hinzugefügt.!",
                guildid=ctx.guild.id,
            )

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @trigger.command(name="remove", aliases=["del", "delete"], usage="<Trigger Name>")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx: commands.Context, *, word):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            if word not in await get_trigger_list(guildid=ctx.guild.id):
                embed = discord.Embed(
                    title=f"**Fehler**",
                    description=f"Der Trigger {word} existiert nicht! Wenn du einen erstellen möchtest,"
                    "nutz den Befehl:"
                    f"```{await get_prefix_string(message=ctx.message)}trigger add```",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)  # todo add components
                await log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                    f"trigger remove zu benutzen und damit den Trigger {word} zu löschen, konnte"
                    f" es aber nicht da dieser nicht existiert hat!",
                    guildid=ctx.guild.id,
                )
                return
            await remove_trigger(guildid=ctx.guild.id, trigger=word)
            embed = discord.Embed(
                title=f"**Trigger Remove**",
                description=f"Der Trigger ```{word}``` mit dem Wert ```{await get_trigger_msg(guildid=ctx.guild.id, trigger=word)}"
                f"```wurde erfolgreich gelöscht.",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                f"trigger remove benutzt und damit den Trigger {word} gelöscht!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @trigger.command(name="edit", usage="<Trigger Name : Antwort Nachricht>")
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx: commands.Context, *, content):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            try:
                word = content.split(" : ")[0]
                msg = content.split(" : ")[1]
            except Exception:

                class error(inspect.Parameter):
                    name = "trigger add"
                    param = "subcommand"

                raise MissingRequiredArgument(error)
            if word not in await get_trigger_list(guildid=ctx.guild.id):
                embed = discord.Embed(
                    title=f"**Fehler**",
                    description=f"Der Trigger {word} existiert nicht! Wenn du einen erstellen möchtest,"
                    "nutz den Befehl:"
                    f"```{await get_prefix_string(message=ctx.message)}trigger add```",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)  # todo add components
                await log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                    f"trigger edit zu benutzen und damit den Trigger {word} zu bearbeiten, konnte"
                    f" es aber nicht da dieser nicht existiert hat!",
                    guildid=ctx.guild.id,
                )
                return
            await add_trigger(guildid=ctx.guild.id, trigger=word, msg=msg)
            embed = discord.Embed(
                title=f"**Trigger edit**",
                description=f"Der Trigger ```{word}``` wurde erfolgreich zu ```{await get_trigger_msg(guildid=ctx.guild.id, trigger=word)}``` geändert.",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                f'trigger add benutzt und damit den Trigger {word} zu "{await get_trigger_msg(guildid=ctx.guild.id, trigger=word)}" bearbeitet!',
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(trigger(bot))
