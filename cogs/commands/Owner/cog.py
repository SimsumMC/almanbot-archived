import os
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from config import THUMBNAIL_URL, WRONG_CHANNEL_ERROR
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
        if await botchannel_check(ctx):
            embed = discord.Embed(
                title="Fehler", colour=await get_embedcolour(ctx.message)
            )
            embed.add_field(
                name="‎",
                value=f"""
                Bitte gib eines der unten angegebenen Befehle ein:
                `{await get_prefix_string(ctx.message)}cog list`
                `{await get_prefix_string(ctx.message)}cog load <Name vom Cog>`
                `{await get_prefix_string(ctx.message)}cog unload <Name vom Cog>`
                `{await get_prefix_string(ctx.message)}cog reload <Name vom Cog>`
                `{await get_prefix_string(ctx.message)}cog reloadall` """,
                inline=False,
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(usage="<Name>")
    @commands.is_owner()
    async def load(self, ctx, cogname):
        if await botchannel_check(ctx):
            try:
                for directory in os.listdir("./cogs"):
                    for directory2 in os.listdir(f"./cogs/{directory}"):
                        for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                            if filename == f"{cogname}.py":
                                extension = (
                                    f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                )
                                client.load_extension(extension)
                                embed = discord.Embed(
                                    title="Cog Load",
                                    colour=await get_embedcolour(ctx.message),
                                )
                                embed.add_field(
                                    name="‎",
                                    value=f"Der Cog ```{cogname}``` konnte erfolgreich geladen werden.",
                                    inline=False,
                                )
                                embed._footer = await get_embed_footer(ctx)
                                embed._thumbnail = await get_embed_thumbnail()
                                await ctx.send(embed=embed)
                                return
                else:
                    embed = discord.Embed(
                        title="Fehler", colour=await get_embedcolour(ctx.message)
                    )
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht gefunden werden.",
                        inline=False,
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Fehler", colour=await get_embedcolour(ctx.message)
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht geladen werden. \n\n"
                    f"Fehler: {str(e)}",
                    inline=False,
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                raise Exception
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(usage="<Name>")
    @commands.is_owner()
    async def unload(self, ctx, cogname):
        if await botchannel_check(ctx):
            try:
                for directory in os.listdir("./cogs"):
                    for directory2 in os.listdir(f"./cogs/{directory}"):
                        for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                            if filename == f"{cogname}.py":
                                extension = (
                                    f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                )
                                client.unload_extension(extension)
                                embed = discord.Embed(
                                    title="Cog Unload",
                                    colour=await get_embedcolour(ctx.message),
                                )
                                embed.add_field(
                                    name="‎",
                                    value=f"Der Cog ```{cogname}``` konnte erfolgreich entladen werden.",
                                    inline=False,
                                )
                                embed._footer = await get_embed_footer(ctx)
                                embed._thumbnail = await get_embed_thumbnail()
                                await ctx.send(embed=embed)
                                return
                else:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=WRONG_CHANNEL_ERROR,
                        colour=await get_embedcolour(message=ctx.message),
                    )
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht entladen werden.",
                        inline=False,
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Fehler", colour=await get_embedcolour(ctx.message)
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht entladen werden. \n\n"
                    f"Fehler: {str(e)}",
                    inline=False,
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(usage="<Name>")
    @commands.is_owner()
    async def reload(self, ctx, cogname):
        user = ctx.author.name
        if await botchannel_check(ctx):
            try:
                for directory in os.listdir("./cogs"):
                    for directory2 in os.listdir(f"./cogs/{directory}"):
                        for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                            if filename == f"{cogname}.py":
                                extension = (
                                    f"cogs.{directory}.{directory2}.{filename[:-3]}"
                                )
                                client.unload_extension(extension)
                                client.load_extension(extension)
                                embed = discord.Embed(
                                    title="Cog Reload",
                                    colour=await get_embedcolour(ctx.message),
                                )
                                embed.set_thumbnail(url=THUMBNAIL_URL)
                                embed.add_field(
                                    name="‎",
                                    value=f"Der Cog ```{cogname}``` konnte erfolgreich neu geladen werden.",
                                    inline=False,
                                )
                                embed._footer = await get_embed_footer(ctx)
                                await ctx.send(embed=embed)
                                return
                else:
                    embed = discord.Embed(
                        title="Fehler", colour=await get_embedcolour(ctx.message)
                    )
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht neu geladen werden.",
                        inline=False,
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Fehler", colour=await get_embedcolour(ctx.message)
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht neu geladen werden. \n\n"
                    f"Fehler: {str(e)}",
                    inline=False,
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(name="reloadall", aliases=["rall", "ra"])
    @commands.is_owner()
    async def reloadall(self, ctx):
        global filename
        if await botchannel_check(ctx):
            for directory in os.listdir("./cogs"):
                for directory2 in os.listdir(f"./cogs/{directory}"):
                    if directory2 == "Ignore":
                        continue
                    for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                        if filename.endswith(".py") and "ignore_" not in filename:
                            extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
                            try:
                                client.unload_extension(extension)
                            except Exception:
                                pass
                            try:
                                client.load_extension(extension)
                            except Exception as e:
                                embed = discord.Embed(
                                    title="Fehler",
                                    colour=await get_embedcolour(ctx.message),
                                )
                                embed.add_field(
                                    name="‎",
                                    value=f"Der Cog ```{filename}``` konnte nicht neu geladen werden. \n\n"
                                    f"Fehler: {str(e)}",
                                    inline=False,
                                )
                                embed._footer = await get_embed_footer(ctx)
                                embed._thumbnail = await get_embed_thumbnail()
                                await ctx.send(embed=embed)
                                traceback.print_exc()

            embed = discord.Embed(
                title="Cog Reload", colour=await get_embedcolour(ctx.message)
            )
            embed.add_field(
                name="‎",
                value=f"Alle Cogs konnte erfolgreich neu geladen werden.",
                inline=False,
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @cog.command(name="list", aliases=["liste", "show", "display", "all"])
    async def list(self, ctx):
        global filename, embed
        description: str = ""
        if await botchannel_check(ctx):
            check = 0
            for directory in os.listdir("./cogs"):
                if check == 0:
                    description = description + f"\n**{directory.capitalize()}**\n\n"
                for directory2 in os.listdir(f"./cogs/{directory}"):
                    if directory2 == "Ignore":
                        continue
                    for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                        if filename.endswith(".py"):
                            extension = f"cogs.{directory}.{directory2}.{filename[:-3]}"
                            try:
                                if extension in client.extensions:
                                    emoji = "🟩"
                                else:
                                    emoji = "🟥"
                                description = description + filename[:-3] + emoji + "\n"
                            except Exception:
                                traceback.print_exc()
                check = 0
            embed = discord.Embed(
                title="Cog Liste",
                description=description,
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(cog(bot))
