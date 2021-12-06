import datetime
import inspect
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot, MissingRequiredArgument

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_levelling import get_levelling_config
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import writejson
from cogs.core.functions.logging import log


class levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="levelling", aliases=["levelsettings"])
    @commands.has_permissions(administrator=True)
    async def levelling(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.levelling_help)

    @levelling.command(name="help", aliases=["hilfe"])
    @commands.has_permissions(administrator=True)
    async def levelling_help(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="Levelling Help",
            description=f"Hier findest du alle Sub-Befehle zum Befehl `{prefix}levelling` !",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name=f"**{prefix}levelling roles**",
            value="Zeigt dir alle Levelling-Rollen an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling settings**",
            value="Zeigt dir alle Settings des Levelsystems an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling toggle < all / messages>**",
            value="Aktiviere / Deaktiviere das Levelsystem / die Nachrichten vom Levelsystem!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling set <Einstellung> <Wert>**",
            value="Weise einer Einstellungsmöglichkeit einen bestimmten Wert zu!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            "levelling hilfe benutzt!",
            guildid=ctx.guild.id,
        )

    @levelling.command(name="roles", aliases=["rollen"])
    @commands.has_permissions(administrator=True)
    async def levelling_roles(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        role_dict = dict(await get_levelling_config(guild=ctx.guild))["roles"]
        role_dict_sorted = sorted(role_dict, key=lambda i: i)
        embed = discord.Embed(
            title="Levelling Roles",
            description="".join(
                [
                    f"Level {lvl}: {(ctx.guild.get_role(role_dict[lvl])).mention}\n"
                    for lvl in role_dict_sorted
                ]
            )
            if role_dict != {}
            else "Keine Levellingrollen konfiguriert!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            "levelling roles benutzt!",
            guildid=ctx.guild.id,
        )

    @levelling.command(name="settings", aliases=["config", "einstellungen"])
    @commands.has_permissions(administrator=True)
    async def levelling_settings(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        levelling_dict: dict = await get_levelling_config(guild=ctx.guild)
        embed = discord.Embed(
            title="Levelling Settings",
            description="Hier findest die derzeitigen Einstellungen zum Levelsystem!",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name="Status",
            value="Aktiviert" if levelling_dict["active"] else "Deaktiviert",
            inline=False,
        )
        embed.add_field(
            name="XP pro Nachricht",
            value=str(levelling_dict["xp_per_message"]) + " XP",
            inline=False,
        )
        embed.add_field(
            name="Cooldown", value=str(levelling_dict["cooldown"]) + "s", inline=False
        )
        nachricht_value = f"""
        Status: {"aktiv" if levelling_dict["messages"]["on"] else "deaktiviert"}
        Modus: {levelling_dict["messages"]["mode"]} {"" if levelling_dict["messages"]["mode"] != "channel" else ctx.guild.get_channel(levelling_dict["messages"]["channel"]).mention}
        Nachricht:
        _{levelling_dict["messages"]["content"]}_
        """
        embed.add_field(name="Nachrichten", value=nachricht_value, inline=False)
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            "levelling settings benutzt!",
            guildid=ctx.guild.id,
        )

    @levelling.group(name="toggle", usage="<all / messages>")
    @commands.has_permissions(administrator=True)
    async def levelling_toggle(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "levelling toggle"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @levelling_toggle.command(name="all", aliases=["system", "levelsystem"])
    @commands.has_permissions(administrator=True)
    async def levelling_toggle_all(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["active"] = not levelling_dict["active"]
        toggle_str = "aktiviert" if levelling_dict["active"] else "deaktiviert"
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Toggle All", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(
            name="‎",
            value=f"Das Levelsystem wurde erfolgreich {toggle_str}!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling toggle all benutzt und damit das Levelsystem {toggle_str}!",
            guildid=ctx.guild.id,
        )

    @levelling_toggle.command(name="messages", aliases=["msgs", "nachrichten"])
    @commands.has_permissions(administrator=True)
    async def levelling_toggle_messages(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["messages"]["on"] = not levelling_dict["messages"]["on"]
        toggle_str = "aktiviert" if levelling_dict["messages"]["on"] else "deaktiviert"
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Toggle Messages", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(
            name="‎",
            value=f"Das Levelsystem-Nachrichten wurden erfolgreich {toggle_str}!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling toggle messages benutzt und damit die Levelsystem-Nachrichten {toggle_str}!",
            guildid=ctx.guild.id,
        )

    @levelling.group(
        name="set",
        aliases=["s"],
        usage="<xp_per_msg / cooldown / message_mode / message_content / roles>",
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "levelling set"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @levelling_set.command(
        name="xp_per_msg", aliases=["xppm", "xp_per_message"], usage="<Anzahl>"
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set_xpm(self, ctx: commands.Context, xp: int):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if xp > 1000:
            embed = discord.Embed(
                title="**Fehler**",
                description="Die XP pro Nachricht können nicht größer als 1000 sein!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set xp_per_message die Xp pro Nachricht auf {xp} zu setzen, überschritt aber das Limit!",
                guildid=ctx.guild.id,
            )
            return
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["xp_per_message"] = xp
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Set XP_PER_MSG", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(
            name="‎",
            value=f"Die XP pro Nachricht wurden auf ```{xp}``` gesetzt!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling set xp_per_msg benutzt und damit die XP pro Message auf {xp} gesetzt!",
            guildid=ctx.guild.id,
        )

    @levelling_set.command(
        name="cooldown", aliases=["c", "slowdown", "verzögerung"], usage="<Sekunden>"
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set_cooldown(self, ctx: commands.Context, cooldown: int):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        if cooldown > 300:
            embed = discord.Embed(
                title="**Fehler**",
                description="Der Cooldown kann nicht größer als 300 Sekunden bzw. 5 Minuten sein!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set cooldown den Cooldown auf {cooldown}s zu setzen, überschritt aber das Limit!",
                guildid=ctx.guild.id,
            )
            return
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["cooldown"] = cooldown
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Set Cooldown", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(
            name="‎",
            value=f"Der Cooldown wurde auf ```{cooldown}s``` gesetzt!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling set cooldown benutzt und damit den Cooldown auf {cooldown}s gesetzt!",
            guildid=ctx.guild.id,
        )

    @levelling_set.command(
        name="message_mode",
        aliases=["msgm", "mode"],
        usage="<same / channel / dm> <opt. #Channel>",
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set_message_mode(
        self, ctx: commands.Context, mode, channel: discord.TextChannel = None
    ):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        mode = str(mode).lower()
        if mode not in ["same", "channel", "dm"]:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Modus {mode} existiert nicht, es muss einer der folgenden sein: ```same, channel, dm```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set message_mode den nicht existierenden Message-Modus auf {mode} zu setzen!",
                guildid=ctx.guild.id,
            )
            return
        elif mode == channel and not channel:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Wenn du den Modus `channel` nutzen möchtest, musst du auch einen dazugehörigen Channel angeben."
                f"In deinem Fall wäre das: {prefix}levelling set message_mode channel <dein #Channel> !",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set message_mode den Message-Mode auf {mode} zu setzen, gab aber keinen Channel an!",
                guildid=ctx.guild.id,
            )
            return
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["messages"]["mode"] = mode
        if mode == "channel":
            levelling_dict["messages"]["channel"] = channel.id
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Set Message Mode",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name="‎",
            value=f"Der Message-Mode wurde auf ```{mode}``` gesetzt!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling set message_mode benutzt und damit den Message Modus auf {mode} gesetzt!",
            guildid=ctx.guild.id,
        )

    @levelling_set.command(
        name="message_content", aliases=["msgc", "content"], usage="<Nachrichtenhalt>"
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set_message_mode(self, ctx: commands.Context, content):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        content = str(content)
        if len(content) > 3000:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Nachrichteninhalt darf nicht größer als 3000 sein (Eingabe: {len(content)})!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set message_content den Message-Content zu verändern, dieser überschritt aber das Zeichenlimit!!",
                guildid=ctx.guild.id,
            )
            return
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["messages"]["content"] = content
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Set Message Content",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name="‎",
            value=f"Der Message-Content wurde erfolgreich geändert!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling set message_mode benutzt und damit den Message Content verändert!",
            guildid=ctx.guild.id,
        )

    @levelling_set.group(
        name="roles", aliases=["rollen", "role"], usage="<add / remove>"
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set_roles(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:

            class error(inspect.Parameter):
                name = "levelling set roles"
                param = "subcommand"

            raise MissingRequiredArgument(error)

    @levelling_set_roles.command(
        name="add", aliases=["hinzufügen"], usage="<Level> <@Rolle>"
    )
    @commands.has_permissions(administrator=True)
    async def levelling_set_roles_add(
        self, ctx: commands.Context, level: int, role: discord.Role
    ):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        if str(level) in levelling_dict:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Es ist bereits eine Rolle für das Level {level} vorhanden, bitte entferne diese erst mit: ```{prefix}levelling set roles remove {level}```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set roles add die bereits vorhandene Rolle {role.name} hinzuzufügen!",
                guildid=ctx.guild.id,
            )
            return
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        levelling_dict["roles"][str(level)] = role.id
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Set Roles Add", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(
            name="‎",
            value=f"Bei Level {level} wurde erfolgreich die Rolle {role.mention} gesetzt!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling set roles add benutzt und damit die Rolle {role.name} zum Level {level} hinzugefügt!",
            guildid=ctx.guild.id,
        )

    @levelling_set_roles.command(name="remove", aliases=["entfernen"], usage="<Level>")
    @commands.has_permissions(administrator=True)
    async def levelling_set_roles_remove(self, ctx: commands.Context, level: int):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        backup_levelling_dict = levelling_dict
        if str(level) not in levelling_dict["roles"]:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Es ist noch keine Rolle für das Level {level} vorhanden, bitte füge erst eine hinzu mit: ```{prefix}levelling set roles add {level} <@Rolle>```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}levelling set roles remove die nicht vorhandene Rolle bei Level {level} hinzuzufügen!",
                guildid=ctx.guild.id,
            )
            return
        levelling_dict = dict(await get_levelling_config(guild=ctx.guild))
        del levelling_dict["roles"][str(level)]
        await writejson(key="levelling", value=levelling_dict, path=path)
        embed = discord.Embed(
            title="Levelling Set Roles Remove",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name="‎",
            value=f"Bei Level {level} wurde erfolgreich die Rolle {ctx.guild.get_role(backup_levelling_dict['roles'][str(level)]).mention} entfernt!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"levelling set roles remove benutzt und damit die Rolle vom Level {level} entfernt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(levelling(bot))
