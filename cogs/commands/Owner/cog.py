import os
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from main import client


class cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx):
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if ctx.invoked_subcommand is None:
            if botchannel_check(ctx):
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.add_field(
                    name="‎",
                    value="Bitte gib eines der unten angegebenen Argumente ein:\n"
                    "`load <Name vom Cog>`\n`unload <Name vom Cog>`\n`reload <Name vom "
                    "Cog>`\n `reloadall`\n",
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
            else:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=WRONG_CHANNEL_ERROR,
                    colour=get_embedcolour(message=ctx.message),
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
                embed.add_field(
                    name="‎",
                    value=get_botchannel_obj_list(ctx),
                    inline=False,
                )
                await ctx.send(embed=embed)
                await msg2.delete()

    @cog.command()
    @commands.is_owner()
    async def load(self, ctx, cogname: str):
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
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
                                    embed.set_thumbnail(url=THUMBNAIL_URL)
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{cogname}``` konnte erfolgreich geladen werden.",
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
                    embed.set_thumbnail(url=THUMBNAIL_URL)
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht geladen werden.",
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
            except Exception:
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.set_thumbnail(
                    url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy"
                    ".png?width=676&height=676"
                )
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht geladen werden.",
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
                raise Exception
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
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
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()

    @load.error
    async def handle_error(self, ctx, error):
        user = ctx.author
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
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
            embed.add_field(
                name="‎",
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "```cog load <Name>```",
                inline=False,
            )
            await ctx.send(embed=embed)

    @cog.command()
    @commands.is_owner()
    async def unload(self, ctx, cogname: str):
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
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
                                    embed.set_thumbnail(url=THUMBNAIL_URL)
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{cogname}``` konnte erfolgreich entladen werden.",
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
                        title="**Fehler**",
                        description=WRONG_CHANNEL_ERROR,
                        colour=get_embedcolour(message=ctx.message),
                    )
                    embed.set_thumbnail(url=THUMBNAIL_URL)
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht entladen werden.",
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
            except Exception:
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht entladen werden.",
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
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
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
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()

    @unload.error
    async def handle_error(self, ctx, error):
        user = ctx.author
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
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
            embed.add_field(
                name="‎",
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "```cog unload <Name>```",
                inline=False,
            )
            await ctx.send(embed=embed)

    @cog.command()
    @commands.is_owner()
    async def reload(self, ctx, cogname: str):
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
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
                    embed.set_thumbnail(url=THUMBNAIL_URL)
                    embed.add_field(
                        name="‎",
                        value=f"Der Cog ```{cogname}``` konnte nicht neu geladen werden.",
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
            except Exception:
                embed = discord.Embed(
                    title="Fehler", colour=get_embedcolour(ctx.message)
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.add_field(
                    name="‎",
                    value=f"Der Cog ```{cogname}``` konnte nicht neu geladen werden.",
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
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
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
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()

    @reload.error
    async def handle_error(self, ctx, error):
        user = ctx.author
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
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
            embed.add_field(
                name="‎",
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "```cog reload <Name>```",
                inline=False,
            )
            await ctx.send(embed=embed)

    @cog.command()
    @commands.is_owner()
    async def reloadall(self, ctx):
        global filename
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            for directory in os.listdir("./cogs"):
                if directory != "Ignore":
                    for directory2 in os.listdir(f"./cogs/{directory}"):
                        for filename in os.listdir(f"./cogs/{directory}/{directory2}/"):
                            if filename.endswith(".py"):
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
                                    embed.set_thumbnail(url=THUMBNAIL_URL)
                                    embed.add_field(
                                        name="‎",
                                        value=f"Der Cog ```{filename}``` konnte nicht neu geladen werden. \n\n"
                                        f"Fehler: {str(e)}",
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
                                    traceback.print_exc()

            embed = discord.Embed(
                title="Cog Reload", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.add_field(
                name="‎",
                value=f"Alle Cogs konnte erfolgreich neu geladen werden.",
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
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
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
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(cog(bot))
