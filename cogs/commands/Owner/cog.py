import os
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.functions import (
    get_author,
)
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from main import client


class cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._help)

    @cog.command(name="help", aliases=["hilfe", "cmds", "commands"])
    @commands.is_owner()
    async def _help(self, ctx):
        if botchannel_check(ctx):
            embed = discord.Embed(title="Fehler", colour=get_embedcolour(ctx.message))
            embed.add_field(
                name="‎",
                value=f"""
                Bitte gib eines der unten angegebenen Befehle ein:
                `{get_prefix_string(ctx.message)}cog list`
                `{get_prefix_string(ctx.message)}cog load <Name vom Cog>`
                `{get_prefix_string(ctx.message)}cog unload <Name vom Cog>`
                `{get_prefix_string(ctx.message)}cog reload <Name vom Cog>`
                `{get_prefix_string(ctx.message)}cog reloadall` """,
                inline=False,
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(usage="<Name>")
    @commands.is_owner()
    async def load(self, ctx, cogname):
        if botchannel_check(ctx):
            try:
                for directory in os.listdir("./cogs"):
                    if directory != "Ignore":
                        for directory2 in os.listdir(f"./cogs/{directory}"):
                            for filename in os.listdir(
                                    f"./cogs/{directory}/{directory2}/"
                            ):
                                if filename == f"{cogname}.py":
                                    extension = (
                                        f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                    )
                                    client.load_extension(extension)
                                    embed = discord.Embed(
                                        title="Cog Load",
                                        colour=get_embedcolour(ctx.message),
                                    )
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{cogname}``` konnte erfolgreich geladen werden.",
                                        inline=False,
                                    )
                                    embed._footer = get_embed_footer(ctx)
                                    embed._thumbnail = get_embed_thumbnail()
                                    await ctx.send(embed=embed)
                                    return
                else:
                    embed = discord.Embed(
                        title="Fehler", colour=get_embedcolour(ctx.message)
                    )
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht gefunden werden.",
                        inline=False,
                    )
                    embed._footer = get_embed_footer(ctx)
                    embed._thumbnail = get_embed_thumbnail()
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht geladen werden. \n\n"
                          f"Fehler: {str(e)}",
                    inline=False,
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)
                raise Exception
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(usage="<Name>")
    @commands.is_owner()
    async def unload(self, ctx, cogname):
        if botchannel_check(ctx):
            try:
                for directory in os.listdir("./cogs"):
                    if directory != "Ignore":
                        for directory2 in os.listdir(f"./cogs/{directory}"):
                            for filename in os.listdir(
                                    f"./cogs/{directory}/{directory2}/"
                            ):
                                if filename == f"{cogname}.py":
                                    extension = (
                                        f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                    )
                                    client.unload_extension(extension)
                                    embed = discord.Embed(
                                        title="Cog Unload",
                                        colour=get_embedcolour(ctx.message),
                                    )
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{cogname}``` konnte erfolgreich entladen werden.",
                                        inline=False,
                                    )
                                    embed._footer = get_embed_footer(ctx)
                                    embed._thumbnail = get_embed_thumbnail()
                                    await ctx.send(embed=embed)
                                    return
                else:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=WRONG_CHANNEL_ERROR,
                        colour=get_embedcolour(message=ctx.message),
                    )
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht entladen werden.",
                        inline=False,
                    )
                    embed._footer = get_embed_footer(ctx)
                    embed._thumbnail = get_embed_thumbnail()
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht entladen werden. \n\n"
                          f"Fehler: {str(e)}",
                    inline=False,
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(usage="<Name>")
    @commands.is_owner()
    async def reload(self, ctx, cogname):
        user = ctx.author.name
        if botchannel_check(ctx):
            try:
                for directory in os.listdir("./cogs"):
                    if directory != "Ignore":
                        for directory2 in os.listdir(f"./cogs/{directory}"):
                            for filename in os.listdir(
                                    f"./cogs/{directory}/{directory2}/"
                            ):
                                if filename == f"{cogname}.py":
                                    extension = (
                                        f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                    )
                                    client.unload_extension(extension)
                                    client.load_extension(extension)
                                    embed = discord.Embed(
                                        title="Cog Reload",
                                        colour=get_embedcolour(ctx.message),
                                    )
                                    embed.set_thumbnail(url=THUMBNAIL_URL)
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{cogname}``` konnte erfolgreich neu geladen werden.",
                                        inline=False,
                                    )
                                    embed.set_footer(
                                        text=FOOTER[0]
                                             + str(user)
                                             + FOOTER[1]
                                             + str(get_author())
                                             + FOOTER[2]
                                             + str(get_prefix_string(ctx.message)),
                                        icon_url=ICON_URL,
                                    )
                                    await ctx.send(embed=embed)
                                    return
                else:
                    embed = discord.Embed(
                        title="Fehler", colour=get_embedcolour(ctx.message)
                    )
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht neu geladen werden.",
                        inline=False,
                    )
                    embed._footer = get_embed_footer(ctx)
                    embed._thumbnail = get_embed_thumbnail()
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht neu geladen werden. \n\n"
                          f"Fehler: {str(e)}",
                    inline=False,
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(name="reloadall", aliases=["rall", "ra"])
    @commands.is_owner()
    async def reloadall(self, ctx):
        global filename
        if botchannel_check(ctx):
            for directory in os.listdir("./cogs"):
                if directory != "Ignore":
                    for directory2 in os.listdir(f"./cogs/{directory}"):
                        for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                            if filename.endswith(".py") and "ignore_" not in filename:
                                extension = (
                                    f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                )
                                try:
                                    client.unload_extension(extension)
                                except Exception:
                                    pass
                                try:
                                    client.load_extension(extension)
                                except Exception as e:
                                    embed = discord.Embed(
                                        title="Fehler",
                                        colour=get_embedcolour(ctx.message),
                                    )
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{filename}``` konnte nicht neu geladen werden. \n\n"
                                              f"Fehler: {str(e)}",
                                        inline=False,
                                    )
                                    embed._footer = get_embed_footer(ctx)
                                    embed._thumbnail = get_embed_thumbnail()
                                    await ctx.send(embed=embed)
                                    traceback.print_exc()

            embed = discord.Embed(
                title="Cog Reload", colour=get_embedcolour(ctx.message)
            )
            embed.add_field(
                name="‎",
                value=f"Alle Cogs konnte erfolgreich neu geladen werden.",
                inline=False,
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(name="list", aliases=["liste", "show", "display", "all"])
    async def list(self, ctx):
        global filename, embed
        description: str = ""
        if botchannel_check(ctx):
            check = 0
            for directory in os.listdir("./cogs"):
                if directory != "Ignore":
                    if check == 0:
                        description = (
                                description + f"\n**{directory.capitalize()}**\n\n"
                        )
                    for directory2 in os.listdir(f"./cogs/{directory}"):
                        for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                            if filename.endswith(".py"):
                                extension = (
                                    f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                )
                                try:
                                    if extension in client.extensions:
                                        emoji = "🟩"
                                    else:
                                        emoji = "🟥"
                                    description = (
                                            description + filename[:-3] + emoji + "\n"
                                    )
                                except Exception:
                                    traceback.print_exc()
                    check = 0
            embed = discord.Embed(
                title="Cog Liste",
                description=description,
                colour=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(cog(bot))
