import datetime
import inspect
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.config.config_autoroles import get_autorole_mentions_list
from cogs.core.config.config_botchannel import get_botchannel_obj_list
from cogs.core.config.config_buttoncolour import (
    translate_buttoncolour,
    get_button_colour_list,
)
from cogs.core.config.config_embedcolour import (
    get_embedcolour,
    colourcode_to_name,
    get_embedcolour_code,
)
from cogs.core.config.config_general import get_config
from cogs.core.config.config_memechannel import get_memechannel_obj_list
from cogs.core.config.config_memes import meme_is_checked, redditnsfwcheck
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.func_json import writejson, readjson
from cogs.core.functions.logging import log
from config import DEFAULT_PREFIX, EMBEDCOLOUR_CODES, EMBEDCOLOURS_SUPPORTED


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cooldown = 5

    @commands.group(name="config", aliases=["settings", "conf", "set"])
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.config_help)

    @config.command(name="help", aliases=["hilfe, commands, befehle, cmds"])
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
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
            name=f"**{prefix}config colour**",
            value="Ändere die Farbe der Embeds und Buttons!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config botchannel**",
            value="Sorge dafür das die Befehle nur in einem bestimmten Kanal funktionieren!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config memechannel**",
            value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config memesource**",
            value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config autoroles**",
            value="Konfiguriere die Rollen die neue Nutzer direkt bekommen sollen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}config autoroles**",
            value="Konfiguriere die Rollen die neue Nutzer direkt bekommen sollen!",
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
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
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
        embed.add_field(
            name="**Prefixes**", value=config_json["prefix"][0], inline=False
        )
        embed.add_field(
            name="**Embed-Farbe**",
            value=await colourcode_to_name(config_json["embedcolour"]),
            inline=False,
        )
        embed.add_field(
            name="**Button-Farbe**",
            value=await translate_buttoncolour(
                language="de", colour=config_json["buttoncolour"]
            ),
            inline=False,
        )
        embed.add_field(
            name="**Standard-Reddit**",
            value=f'[{config_json["memesource"]}](https://www.reddit.com/r/{config_json["memesource"]})',
            inline=False,
        )
        embed.add_field(name="**Blacklist**", value="a!blacklist list", inline=False)
        embed.add_field(name="**Triggerlist**", value="a!trigger list", inline=False)
        embed.add_field(
            name="**Botchannel**",
            value=str(await get_botchannel_obj_list(ctx))
            if await get_botchannel_obj_list(ctx)
            else "Nicht definiert",
            inline=False,
        )
        embed.add_field(
            name="**Memechannel**",
            value=str(await get_memechannel_obj_list(ctx))
            if await get_memechannel_obj_list(ctx)
            else "Nicht definiert",
            inline=False,
        )
        embed.add_field(
            name="**Autoroles**",
            value=await get_autorole_mentions_list(guild=ctx.guild),
            inline=False)
        embed.add_field(
            name="**Levelsystem**",
            value=f"Mehr Infos unter {await get_prefix_string(ctx.message)}levelling und {await get_prefix_string(ctx.message)}levelling roles!",
            inline=False,
            )
        embed.add_field(
            name="**Deaktivierte Befehle**",
            value="".join([cmd + ", " for cmd in config_json["deactivated_commands"]])[
                :-2
            ]
            if config_json["deactivated_commands"]
            else "Aktuell sind keine Befehle deaktiviert!",
            inline=False,
        )
        embed.add_field(
            name="**Error-Typen**",
            value="".join(
                [
                    str(config_json["errors"][e]) + " : " + e + "\n"
                    for e in config_json["errors"]
                ]
            )
            .replace("False", "🔴")
            .replace("True", "🟢"),
            inline=False,
        )
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
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_prefix(self, ctx, arg=DEFAULT_PREFIX):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if prefix == arg:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Präfix muss sich vom aktuellen unterscheiden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config prefix versucht den Prefix zum aktuellen Wert zu ändern! ",
                ctx.guild.id,
            )
            return
        elif len(arg) > 16:
            embed = discord.Embed(
                title="**Fehler**",
                description=f'Der Präfix darf maximal 16 Zeichen lang sein, daher ist dein eingegebener Präfix "`{arg}`" ungültig.',
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config prefix versucht den Prefix zu ändern, der eingegebene Wert war aber länger als 16 Zeichen ({len(arg)})! ",
                ctx.guild.id,
            )
            return
        await writejson(key="prefix", value=[str(arg)], path=path)
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

    @config.group(
        name="colour",
        aliases=["farbe", "color", "farben"],
        usage="<Embed / Button> <set / list>",
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config colour"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_colour.group(
        name="embed", aliases=["msg", "message", "nachricht"], usage="<set / list>"
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour_embed(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config colour embed"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_colour_embed.command(name="set", aliases=["s"], usage="<Farbe>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour_embed_set(self, ctx, colour):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if colour.lower() not in EMBEDCOLOURS_SUPPORTED:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Die Farbe ```{str(colour.lower()).capitalize()}``` existiert nicht!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}config colour embed set zu benutzen, hat aber eine ungütige Farbe angegeben!",
                ctx.guild.id,
            )
            return
        await writejson(
            key="embedcolour",
            value=await get_embedcolour_code(colour.lower()),
            path=path,
        )
        embed = discord.Embed(
            title="**Config Colour**",
            description=f"Die Embed-Farbe wurde nun zu ```{str(colour.lower()).capitalize()}``` geändert!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {await get_prefix_string(ctx.message)}"
            f"config colour embed set die Farbe zu {str(colour.lower()).capitalize()} geändert!",
            guildid=ctx.guild.id,
        )

    @config_colour_embed.command(name="list", aliases=["l", "all", "liste"])
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour_embed_list(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        colours = "".join([colour.capitalize() + ", " for colour in EMBEDCOLOUR_CODES])[
            :-2
        ]
        embed = discord.Embed(
            title="**Config Colour**",
            description=colours,
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "config colour embed list benutzt!",
            guildid=ctx.guild.id,
        )

    @config_colour.group(name="button", aliases=["knopf", "b"], usage="<set / list>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour_button(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config colour button"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_colour_button.command(name="set", aliases=["s"], usage="<Farbe>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour_button_set(self, ctx, colour):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if colour.lower() in await get_button_colour_list("en"):
            buttoncolour = colour.lower()
        elif colour.lower() in await get_button_colour_list("de"):
            buttoncolour = await translate_buttoncolour(
                language="en", colour=colour.lower()
            )
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Die Farbe ```{str(colour.lower()).capitalize()}``` existiert nicht!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}config colour button set zu benutzen, hat aber eine ungütige Farbe angegeben!",
                ctx.guild.id,
            )
            return
        await writejson(key="buttoncolour", value=str(buttoncolour), path=path)
        embed = discord.Embed(
            title="**Config Colour**",
            description=f"Die Button-Farbe wurde nun zu ```{str(colour.lower()).capitalize()}``` geändert!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {await get_prefix_string(ctx.message)}"
            f"config colour button set die Button-Farbe zu {str(colour.lower()).capitalize()} geändert!",
            guildid=ctx.guild.id,
        )

    @config_colour_button.command(name="list", aliases=["l", "all", "liste"])
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_colour_button_list(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        colours = "".join(
            [
                colour.capitalize() + ", "
                for colour in await get_button_colour_list("de")
            ]
        )[:-2]
        embed = discord.Embed(
            title="**Config Colour**",
            description=colours,
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "config colour button list benutzt!",
            guildid=ctx.guild.id,
        )

    @config.group(
        name="botchannel",
        aliases=["bot", "botchat", "botkanal"],
        usage="add/remove <@Channel>",
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_botchannel(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config botchannel"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_botchannel.command(name="add", aliases=["hinzufügen"], usage="<@Channel>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_botchannel_add(self, ctx, channel: discord.TextChannel):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        botchannel = await readjson(key="botchannel", path=path)
        if channel.id in botchannel:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Channel {channel.mention} ist breits auf der Botchannel-Liste!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config botchannel add versucht den bereits vorhandenen Channel {channel.name} auf die Botchannel-Liste hinzuzufügen!",
                ctx.guild.id,
            )
            return
        await writejson(key="botchannel", value=channel.id, path=path, mode="append")
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

    @config_botchannel.command(
        name="remove", aliases=["entfernen", "r"], usage="<@Channel>"
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_botchannel_remove(self, ctx, channel: discord.TextChannel):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        botchannel = await readjson(key="botchannel", path=path)
        if channel.id not in botchannel:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Channel {channel.mention} ist nicht auf der Memechannel-Liste vorhanden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config memechannel versucht den nicht gesetzten Channel {channel.name} auf die Memechannel-Liste zu packen!",
                ctx.guild.id,
            )
            return
        await writejson(key="botchannel", value=channel.id, path=path, mode="remove")
        embed = discord.Embed(
            title="**Config Botchannel**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich von der Memechannel-Liste entfernt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'memechannel remove den Channel "{channel.name}" von der Memechannel-Liste entfernt.',
            guildid=ctx.guild.id,
        )

    @config.group(
        name="memechannel",
        aliases=["meme", "memechat", "memekanal"],
        usage="add/remove <@channel>",
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_memechannel(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config memechannel"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_memechannel.command(name="add", aliases=["hinzufügen"], usage="<@Channel>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_memechannel_add(self, ctx, channel: discord.TextChannel):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        memechannel = await readjson(key="botchannel", path=path)
        if channel.id in memechannel:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Channel {channel.mention} ist breits auf der Memechannel-Liste!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config memechannel add versucht den bereits vorhandenen Channel {channel.name} auf die Memechannel-Liste hinzuzufügen!",
                ctx.guild.id,
            )
            return
        await writejson(key="memechannel", value=channel.id, path=path, mode="append")
        embed = discord.Embed(
            title="**Config Memechannel**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich zu der Memechannel-Liste hinzugefügt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'memechannel add den Channel "{channel.name}" zu der Memechannel-Liste hinzugefügt.',
            guildid=ctx.guild.id,
        )

    @config_memechannel.command(
        name="remove", aliases=["entfernen"], usage="<@Channel>"
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_memechannel_remove(
        self, ctx: commands.Context, channel: discord.TextChannel
    ):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        memechannel = await readjson(key="memechannel", path=path)
        if channel.id not in memechannel:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Channel {channel.mention} ist nicht auf der Memechannel-Liste vorhanden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config memechannel versucht den nicht gesetzten Channel {channel.name} auf die Memechannel-Liste zu packen!",
                ctx.guild.id,
            )
            return
        await writejson(key="memechannel", value=channel.id, path=path, mode="remove")
        embed = discord.Embed(
            title="**Config Memechannel**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Channel ```{channel.name}``` wurde erfolgreich von der Memechannel-Liste entfernt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'memechannel remove den Channel "{channel.name}" von der Memechannel-Liste entfernt.',
            guildid=ctx.guild.id,
        )

    @config.group(
        name="autoroles",
        aliases=["autorole", "roles", "rollen"],
        usage="<add / remove>",
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_autoroles(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config autoroles"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_autoroles.command(name="add", aliases=["hinzufügen"], usage="<@Role>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_autoroles_add(self, ctx: commands.Context, role: discord.Role):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        autoroles = await readjson(key="autoroles", path=path)
        if ctx.author.top_role < role and ctx.author.roles[1:]:
            embed = discord.Embed(
                title="Fehler",
                description="Du bist in der Hierarchie unter der Rolle die du zu den Autoroles hinzufügen willst, daher bist du zu dieser Aktion nicht berechtigt!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht die Rolle {role} mit dem"
                f" Befehl {await get_prefix_string(ctx.message)}config autoroles add zu den Autoroles hinzuzufügen, war jedoch dazu nicht berrechtigt.",
                ctx.guild.id,
            )
            return
        if role.id in autoroles:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Die Rolle {role.mention} ist bereits auf der Autoroles-Liste!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config autoroles add versucht die bereits vorhandene Rolle {role.name} auf die Autoroles-Liste hinzuzufügen!",
                ctx.guild.id,
            )
            return
        if role.name == "@everyone":
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Die Rolle {role.mention} kann nicht hinzugefügt werden, da diese die Standardrolle von Discord ist!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config autoroles add versucht die Standardroll (@everyone) auf die Autoroles-Liste hinzuzufügen!",
                ctx.guild.id,
            )
            return
        await writejson(key="autoroles", value=role.id, path=path, mode="append")
        embed = discord.Embed(
            title="**Config Autoroles**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Die Rolle {role.mention} wurde erfolgreich zu der Autorole-Liste hinzugefügt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'autoroles add die Rolle "{role.name}" zu der Autoroles-Liste hinzugefügt.',
            guildid=ctx.guild.id,
        )

    @config_autoroles.command(
        name="remove", aliases=["entfernen", "r"], usage="<@Role>"
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_autoroles_remove(self, ctx: commands.Context, role: discord.Role):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        autoroles = await readjson(key="autoroles", path=path)
        if ctx.author.top_role < role and ctx.author.roles[1:]:
            embed = discord.Embed(
                title="Fehler",
                description="Du bist in der Hierarchie unter der Rolle die du zu den Autoroles entfernen willst, daher bist du zu dieser Aktion nicht berechtigt!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht die Rolle {role} mit dem"
                f" Befehl {await get_prefix_string(ctx.message)}config autoroles remove von den Autoroles zu entfernen, war jedoch dazu nicht berrechtigt.",
                ctx.guild.id,
            )
            return
        if role.id not in autoroles:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Die Rolle {role.mention} ist nicht auf der Autoroles-Liste, um eine Rolle zu entfernen muss diese erst hinzugefügt werden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config autoroles remove versucht die nicht vorhandene Rolle {role.name} von der Autoroles-Liste zu entfernen!",
                ctx.guild.id,
            )
            return
        await writejson(key="autoroles", value=role.id, path=path, mode="remove")
        embed = discord.Embed(
            title="**Config Autoroles**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Die Rolle {role.mention} wurde erfolgreich von der Autorole-Liste entfernt.",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'autoroles remove die Rolle "{role.name}" von der Autoroles-Liste entfernt.',
            guildid=ctx.guild.id,
        )

    @config.command(
        name="memesource",
        aliases=["reddit", "memequelle", "r"],
        usage="<add / remove / list>",
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_memesource(self, ctx, reddit):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        memesource = await readjson(key="autoroles", path=path)
        if str(reddit.lower()) == memesource:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der aktuelle Reddit für den Meme-Befehl ist bereits ```r/{reddit}```!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config memesource versucht den Reddit zu ändern, dieser hatte aber breits den gleichen Wert!",
                ctx.guild.id,
            )
            return
        try:
            if await meme_is_checked(str(reddit.lower())) or await redditnsfwcheck(
                reddit=str(reddit.lower())
            ):
                await writejson(
                    key="memesource", value=str(reddit.lower), path=path, mode="remove"
                )
                embed = discord.Embed(
                    title="**Config Memequelle**",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value=f"Der Reddit für den Meme-Befehl wurde erfolgreich zu ```{reddit}``` geändert!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
                    f'config memesource den Meme-Reddit zu "{reddit}" geändert.',
                    guildid=ctx.guild.id,
                )
            else:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=f"Der Reddit ```r/{reddit}``` enthält nciht jugendfreien Inhalt und kann daher nicht als Meme-Reddit genutzt werden!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config memesource versucht den Reddit zu ändern, dieser enthielt aber NSFW Inhalte!",
                    ctx.guild.id,
                )
                return
        except Exception:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Beim Reddit **{reddit}** ist wohl etwas schiefgelaufen. "
                "Das könnte z.B. bedeuten das der Reddit nicht existiert oder das der Reddit "
                "aufgrund von zu vielen Anfragen nicht automatisch auf NSFW Content überprüft "
                "wurde. Sollte letzteres zutreffen, warte ein paar Minuten!",
                color=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat beim Befehl"
                f"'{await get_prefix_string(ctx.message)}meme ein ungültiges Argument eingegeben.",
                ctx.guild.id,
            )

    @config.group(name="error", aliases=["fehler", "errors"], usage="<toogle / list>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_error(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config error"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_error.command(name="toggle", usage="<Error>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_error_toggle(self, ctx, error):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        errors = await readjson(path=path, key="errors")
        if str(error.lower()) not in errors:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Error-Typ ```{str(error)}``` existiert nicht!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config error toggle versucht den nicht exsitierenden Error-Typ {error} zu togglen!",
                ctx.guild.id,
            )
            return
        errors[str(error.lower())] = not errors[str(error.lower())]
        action = "aktiviert" if errors[str(error.lower())] else "deaktivert"
        await writejson(key="errors", value=errors, path=path)
        embed = discord.Embed(
            title="**Config Errors**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Error-Typ ```{error}``` wurde erfolgreich {action}!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'config error toggle den Error-Typ "{error}" {action}.',
            guildid=ctx.guild.id,
        )

    @config_error.command(name="list", aliases=["all", "show"])
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_error_list(self, ctx: commands.Context):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        errors = await readjson(path=path, key="errors")
        embed = discord.Embed(
            title="**Config Error**",
            description="".join([str(errors[e]) + " : " + e + "\n" for e in errors])
            .replace("False", "🔴")
            .replace("True", "🟢"),
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f"config error list sich die Error-Typ Konfiguration anzeigen lassen.",
            guildid=ctx.guild.id,
        )

    @config.group(
        name="commands", aliases=["command", "befehl", "cmd"], usage="<toogle / list>"
    )
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_command(self, ctx):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "config command"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @config_command.command(name="toggle", usage="<Error>")
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_command_toggle(self, ctx, *, cmd):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        deactivated_cmds = await readjson(path=path, key="deactivated_commands")
        blocked = ["config", "broadcast", "cog", "adminconfig", "adminresetconfig"]
        cmd = self.bot.get_command(str(cmd.lower()))
        if not cmd:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Befehl ```{str(cmd)}``` existiert nicht!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config commands toggle versucht den nicht exsitierenden Befehl {cmd} zu togglen!",
                ctx.guild.id,
            )
            return
        elif str(cmd).startswith("config") or str(cmd) in blocked:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Befehl ```{str(cmd)}``` kann nicht getoggelt werden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}config commands toggle versucht den Befehl {cmd} zu togglen, dieser unterstützt das Feature aber nicht!",
                ctx.guild.id,
            )
            return
        if cmd.name.lower() in deactivated_cmds:
            deactivated_cmds.remove(cmd.name.lower())
        else:
            deactivated_cmds.append(cmd.name.lower())
        action = (
            "aktiviert" if cmd.name.lower() not in deactivated_cmds else "deaktivert"
        )
        await writejson(key="deactivated_commands", value=deactivated_cmds, path=path)
        embed = discord.Embed(
            title="**Config Commands**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="‎",
            value=f"Der Befehl ```{cmd}``` wurde erfolgreich {action}!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f'config commands toggle den Befehl "{cmd}" {action}.',
            guildid=ctx.guild.id,
        )

    @config_command.command(name="list", aliases=["all", "show"])
    @commands.cooldown(1, cooldown, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def config_command_list(self, ctx: commands.Context):
        prefix = await get_prefix_string(ctx.message)
        time = datetime.datetime.now()
        user = ctx.author.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        cmds = await readjson(path=path, key="deactivated_commands")
        embed = discord.Embed(
            title="**Config Commands**", colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        embed.add_field(
            name="Deaktivierte Befehle: ",
            value="".join([cmd + ", " for cmd in cmds])[:-2]
            if cmds
            else "Aktuell sind keine Befehle deaktiviert!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit dem Befehl {prefix}"
            f"config commands list sich die dekativierten Befehle anzeigen lassen.",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(config(bot))
