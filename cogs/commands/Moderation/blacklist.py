import asyncio
import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.func_json import writejson, readjson
from cogs.core.functions.logging import log
from config import BLACKLIST_DELETE_AFTER


class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="blacklist", aliases=["autodelete"])
    @commands.has_permissions(ban_members=True)
    async def blacklist(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.blacklist_help)

    @blacklist.command(name="hilfe", aliases=["help"])
    @commands.has_permissions(ban_members=True)
    async def blacklist_help(self, ctx: commands.Context):
        time = datetime.datetime.now()
        user = ctx.author.name
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="**Blacklist Help**",
            description="Hier findest du alle Subbefehle ",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name=f"**{prefix}blacklist help**",
            value="Zeigt dir diese Hilfeseite an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}blacklist list**",
            value="Zeigt dir alle Wörter der Blacklist an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}blacklist add <Wort>**",
            value="Fügt ein Wort zur Blacklist hinzu!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}blacklist remove**",
            value="Entfernt ein Wort von der Blacklist!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}blacklist reset**",
            value="Entfernt _alle_ Wörter von der Blacklist!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix} benutzt!",
            guildid=ctx.guild.id,
        )

    @blacklist.command(name="add", aliases=["hinzufügen", "a"], usage="<Wort>")
    @commands.has_permissions(ban_members=True)
    async def blacklist_add(self, ctx: commands.Context, word):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        bannedWords = await readjson(key="blacklist", path=path)
        await ctx.message.delete()
        if word.lower() in bannedWords:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Das Wort ```{word}```" " ist bereits auf der Blacklist!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed, delete_after=BLACKLIST_DELETE_AFTER)
            await log(
                f'{time}: Der Moderator {user} hat versucht das Wort "{word}" zur Blacklist hinzufügen,'
                " es war aber bereits vorhanden.",
                guildid=ctx.guild.id,
            )
        else:
            await writejson(
                key="blacklist", value=word.lower(), path=path, mode="append"
            )
            embed = discord.Embed(
                title="**Blacklist**",
                description=f"Das Wort ```{word}```"
                " wurde zur Blacklist hinzugefügt!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed, delete_after=BLACKLIST_DELETE_AFTER)
            await log(
                f'{time}: Der Moderator {user} hat das Wort "{word}" auf die Blacklist hinzugefügt.',
                guildid=ctx.guild.id,
            )

    @blacklist.command(name="remove", aliases=["entfernen", "r"], usage="<Wort>")
    @commands.has_permissions(ban_members=True)
    async def blacklist_remove(self, ctx: commands.Context, word):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        bannedWords = await readjson(key="blacklist", path=path)
        await ctx.message.delete()
        if word.lower() in bannedWords:
            await writejson(
                key="blacklist", value=word.lower(), path=path, mode="removed"
            )
            embed = discord.Embed(
                title="**Blacklist**",
                description=f"Das Wort ```{word}```"
                " wurde von der Blacklist entfernt!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed, delete_after=BLACKLIST_DELETE_AFTER)
            await log(
                f'{time}: Der Moderator {user} hat das Wort "{word}"von der Blacklist entfernt.',
                guildid=ctx.guild.id,
            )
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Das Wort ```{word}```"
                " befindet sich nicht auf der Blacklist!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed, delete_after=BLACKLIST_DELETE_AFTER)
            await log(
                f'{time}: Der Moderator {user} hat versucht das Wort "{word}" von der Blacklist zu entfernen,'
                " es war aber nicht drauf.",
                guildid=ctx.guild.id,
            )

    @blacklist.command(name="list", aliases=["show", "all", "anzeige"])
    @commands.has_permissions(ban_members=True)
    async def blacklist_list(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        bannedWords = await readjson(key="blacklist", path=path)
        embed = discord.Embed(
            title="**Blacklist List**",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name="‎",
            value="".join([word + ", " for word in bannedWords])[:-2]
            if bannedWords != []
            else "Keine Wörter vorhanden!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Moderator {user} hat sich mit dem Befehl {await get_prefix_string(ctx.message)}blacklist list die Blacklist ausgeben lassen!",
            guildid=ctx.guild.id,
        )

    @blacklist.command(
        name="reset", aliases=["c", "del", "delete", "clear", "zurücksetzen"]
    )
    @commands.has_permissions(ban_members=True)
    async def blacklist_reset(self, ctx: commands.Context):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        bannedWords = await readjson(key="blacklist", path=path)
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        elif not bannedWords:
            embed = discord.Embed(
                title="**Fehler**",
                description="Die Blacklist enthält keine Wörter und somit kann auch nichts gelöscht werden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}blacklist reset die Blacklist zurückzusetzen, diese war aber bereits leer.",
                guildid=ctx.guild.id,
            )
            return
        await writejson(key="blacklist", value=[], path=path)
        embed = discord.Embed(
            title="**Blacklist Reset**",
            description="Die Blacklist wurde erfolgreich zurückgesetzt.",
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
                    custom_id="restore-blacklist",
                )
            ],
        )
        try:
            res = await self.bot.wait_for(
                event="button_click",
                timeout=15.0,
                check=lambda inter: inter.custom_id == "restore-blacklist"
                and inter.message.id == msg.id
                and inter.author.id == ctx.author.id,
            )
            await writejson(key="blacklist", value=bannedWords, path=path)
            await res.respond(
                content="Die Blacklist wurde erfolgreich wiederhergestellt!"
            )
            await log(
                f'{time}: Der Nutzer {user} hat mit dem Button "Wiederherstellung" die Blacklist nach dem Löschvorgang wiederhergestellt!',
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


########################################################################################################################


def setup(bot):
    bot.add_cog(blacklist(bot))
