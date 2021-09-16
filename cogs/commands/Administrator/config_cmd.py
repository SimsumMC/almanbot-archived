import datetime
import inspect
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.config.config_autoroles import get_role_mentions_list
from cogs.core.config.config_botchannel import get_botchannel_obj_list
from cogs.core.config.config_buttoncolour import get_buttoncolour_german
from cogs.core.config.config_embedcolour import (
    get_embedcolour, colourcode_to_name,
)
from cogs.core.config.config_general import get_config
from cogs.core.config.config_memechannel import get_memechannel_obj_list
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.func_json import writejson
from cogs.core.functions.logging import log
from config import DEFAULT_PREFIX


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        embed = discord.Embed(
            title="**Config Hilfe**",
            description=f"Hier findest du alle Subbefehle zum {prefix} config Befehl!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name=f"**{prefix}config prefix <Präfix>**",
            value="Ändere den Prefix deines Bots!",
            inline=False,
        )
        embed.add_field(
            name=f'**{prefix}config colour <Farbe ({prefix}colours / "random">**',
            value="Ändere die Farbe der Embeds!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config botchannel add/remove <@channel>**",
            value="Sorge dafür das die Befehle nur in einem bestimmten Kanal funktionieren!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config memechannel add/remove <@channel>**",
            value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
            inline=False,
        )
        embed.add_field(
            name=f'**{prefix}config memesource <Reddit Name / "default"'
                 ">**",
            value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            text=str(time)
                 + ": Der Nutzer "
                 + str(user)
                 + " hat den Befehl "
                 + prefix
                 + "config hilfe benutzt.",
            guildid=ctx.guild.id,
        )

    @config.command(name="show", aliases=["werte", "s", "all"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_show(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        embed = discord.Embed(
            title="**Config Show**",
            description=f"Hier findest du die Konfiguration deines Servers!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        config_json = await get_config(guildid=ctx.guild.id)
        embed.add_field(name="**Prefix**", value=config_json["prefix"], inline=False)
        embed.add_field(name="**Embed-Farbe**", value=await colourcode_to_name(config_json["embedcolour"]),
                        inline=False)
        embed.add_field(name="**Button-Farbe**", value=await get_buttoncolour_german(config_json["buttoncolour"]),
                        inline=False)
        embed.add_field(name="**Blacklist**",
                        value="".join([word + ", " for word in config_json["blacklist"]])[:-2] if config_json[
                                                                                                      "blacklist"] != [] else "Keine Wörter vorhanden"
                        , inline=False)
        embed.add_field(name="**Botchannel**",
                        value=str(await get_botchannel_obj_list(ctx)) if await get_botchannel_obj_list(
                            ctx) else "Nicht definiert", inline=False)
        embed.add_field(name="**Memechannel**",
                        value=str(await get_memechannel_obj_list(ctx)) if await get_memechannel_obj_list(
                            ctx) else "Nicht definiert", inline=False)
        embed.add_field(name="**Autoroles**", value=await get_role_mentions_list(guild=ctx.guild), inline=False)
        await ctx.send(embed=embed)
        await log(
            text=str(time)
                 + ": Der Nutzer "
                 + str(user)
                 + " hat den Befehl "
                 + await get_prefix_string(ctx.message)
                 + "config hilfe benutzt.",
            guildid=ctx.guild.id,
        )

    @config.command(name="prefix", aliases=["präfix"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_prefix(self, ctx, arg=DEFAULT_PREFIX):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if len(arg) > 16:
            embed = discord.Embed(
                title="**Fehler**",
                description=f'Der Präfix darf maximal 16 Zeichen lang sein, daher ist dein eingegebener Präfix "`{arg}`" ungültig.',
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        await writejson(type="prefix", input=arg, path=path)
        embed = discord.Embed(
            title="**Config Prefix**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Prefix wurde erfolgreich zu ```{arg}``` geändert.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'config den Prefix zu "{arg}" geändert!',
            guildid=ctx.guild.id,
        )

    @config.group(name="botchannel", aliases=["bot"], usage="add/remove <@channel>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config_botchannel(self, ctx):
        if ctx.invoked_subcommand is None:
            class error(inspect.Parameter):
                name = "config botchannel"
                param = "subcommand"
            raise MissingRequiredArgument(error)

    @config_botchannel.command(name="add", aliases=["hinzufügen"])
    async def config_botchannel_add(self, ctx, channel: discord.TextChannel):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        await writejson(type="botchannel", input=channel.id, path=path, mode="append")
        embed = discord.Embed(
            title="**Config Botchannel**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich zu der Botchannel-Liste hinzugefügt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'botchannel add den Channel "{channel.name}" zu der Botchannel-Liste hinzugefügt.',
            guildid=ctx.guild.id,
        )

    @config_botchannel.command(name="remove", aliases=["entfernen"])
    async def config_botchannel_remove(self, ctx, channel: discord.TextChannel):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        await writejson(type="botchannel", input=channel.id, path=path, mode="remove")
        embed = discord.Embed(
            title="**Config Botchannel**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich von der Botchannel-Liste entfernt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'botchannel remove den Channel "{channel.name}" von der Botchannel-Liste entfernt.',
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(config(bot))
