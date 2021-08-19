import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument

from config import ICON_URL, THUMBNAIL_URL, FOOTER, DEFAULT_PREFIX
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.func_json import writejson, readjson
from cogs.core.config.config_memes import get_memes, redditnsfwcheck, meme_is_checked
from cogs.core.config.config_embedcolour import (
    get_embedcolour,
    get_embedcolour_code,
    embedcolour_check,
)
from cogs.core.functions.logging import log


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="config", aliases=["settings", "conf", "set"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.config_help(self, ctx)

    @config.command(name="help", aliases=["hilfe, commands, befehle, cmds"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_help(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        embed = discord.Embed(
            title="**Config Hilfe**",
            description=f"Hier findest du alle Subbefehle zum {get_prefix_string(ctx.message)} config Befehl!",
            colour=get_embedcolour(ctx.message),
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
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
            name=f"**{get_prefix_string(ctx.message)}config prefix <Präfix>**",
            value="Ändere den Prefix deines Bots!",
            inline=False,
        )
        embed.add_field(
            name=f'**{get_prefix_string(ctx.message)}config colour <Farbe ({get_prefix_string(ctx.message)}colours / "random">**',
            value="Ändere die Farbe der Embeds!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(ctx.message)}config botchannel add/remove <@channel>**",
            value="Sorge dafür das die Befehle nur in einem bestimmten Kanal funktionieren!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(ctx.message)}config memechannel add/remove <@channel>**",
            value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
            inline=False,
        )
        embed.add_field(
            name=f'**{get_prefix_string(ctx.message)}config memesource <Reddit Name / "default"'
                 ">**",
            value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            input=str(time)
                  + ": Der Nutzer "
                  + str(user)
                  + " hat den Befehl "
                  + get_prefix_string(ctx.message)
                  + "config hilfe benutzt.",
            id=ctx.guild.id,
        )

    @config.command(name="prefix", aliases=["präfix"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_prefix(self, ctx, arg=DEFAULT_PREFIX):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        writejson(type="prefix", input=arg, path=path)
        embed = discord.Embed(
            title="**Config Prefix**", colour=get_embedcolour(ctx.message)
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
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
            value=f"Der Prefix wurde erfolgreich zu ```{arg}``` geändert.",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {get_prefix_string(ctx.message)}"
            f'config den Prefix zu "{arg}" geändert!',
            id=ctx.guild.id,
        )

    @config.group(name="botchannel")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_botchannel(self, ctx):
        if ctx.invoked_subcommand is None:
            print("none")
            pass
            # todo error missing

    @config_botchannel.command(name="add", aliases=["hinzufügen"])
    async def config_botchannel_add(self, ctx, channel: discord.TextChannel):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        writejson(type="botchannel", input=channel.id, path=path, mode="append")
        embed = discord.Embed(
            title="**Config Botchannel**", colour=get_embedcolour(ctx.message)
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
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
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich zu der Botchannel-Liste hinzugefügt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {get_prefix_string(ctx.message)}"
            f'botchannel add den Channel "{channel.name}" zu der Botchannel-Liste hinzugefügt.',
            id=ctx.guild.id,
        )

    @config_botchannel.command(name="remove", aliases=["entfernen"])
    async def config_botchannel_remove(self, ctx, channel: discord.TextChannel):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        writejson(type="botchannel", input=channel.id, path=path, mode="remove")
        embed = discord.Embed(
            title="**Config Botchannel**", colour=get_embedcolour(ctx.message)
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
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
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich von der Botchannel-Liste entfernt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {get_prefix_string(ctx.message)}"
            f'botchannel remove den Channel "{channel.name}" von der Botchannel-Liste entfernt.',
            id=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(config(bot))
