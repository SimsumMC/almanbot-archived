import datetime
import inspect
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.config.config_embedcolour import (
    get_embedcolour,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.func_json import writejson
from cogs.core.functions.logging import log
from config import DEFAULT_PREFIX


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def on_unload(self):
        print("test")

    @commands.group(name="config", aliases=["settings", "conf", "set"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.config_help)

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
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
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
            text=str(time)
                 + ": Der Nutzer "
                 + str(user)
                 + " hat den Befehl "
                 + get_prefix_string(ctx.message)
                 + "config hilfe benutzt.",
            guildid=ctx.guild.id,
        )

    @config.command(name="prefix", aliases=["präfix"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_prefix(self, ctx, arg=DEFAULT_PREFIX):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if len(arg) > 16:
            embed = discord.Embed(
                title="**Fehler**",
                description=f'Der Präfix darf maximal 16 Zeichen lang sein, daher ist dein eingegebener Präfix "`{arg}`" ungültig.',
                colour=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        writejson(type="prefix", input=arg, path=path)
        embed = discord.Embed(
            title="**Config Prefix**", colour=get_embedcolour(ctx.message)
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Prefix wurde erfolgreich zu ```{arg}``` geändert.",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {get_prefix_string(ctx.message)}"
            f'config den Prefix zu "{arg}" geändert!',
            guildid=ctx.guild.id,
        )

    @config.group(name="botchannel", aliases=["bot"], usage="add/remove <@channel>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_botchannel(self, ctx):
        if ctx.invoked_subcommand is None:
            class error(inspect.Parameter):
                name = "subcommand"

            raise MissingRequiredArgument(error)

    @config_botchannel.command(name="add", aliases=["hinzufügen"])
    async def config_botchannel_add(self, ctx, channel: discord.TextChannel):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        writejson(type="botchannel", input=channel.id, path=path, mode="append")
        embed = discord.Embed(
            title="**Config Botchannel**", colour=get_embedcolour(ctx.message)
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich zu der Botchannel-Liste hinzugefügt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {get_prefix_string(ctx.message)}"
            f'botchannel add den Channel "{channel.name}" zu der Botchannel-Liste hinzugefügt.',
            guildid=ctx.guild.id,
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
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich von der Botchannel-Liste entfernt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {get_prefix_string(ctx.message)}"
            f'botchannel remove den Channel "{channel.name}" von der Botchannel-Liste entfernt.',
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(config(bot))
