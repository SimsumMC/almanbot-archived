import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import readjson
from config import STATCORD_TOKEN


class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="dev", aliases=["owner"])
    @commands.is_owner()
    async def dev(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.help)

    @dev.command(name="help", aliases=["hilfe"])
    @commands.is_owner()
    async def help(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="**[Dev] Hilfe**", description=f"Hier findest du alle Sub-Befehle zum `{prefix}dev help` Befehl!",
            colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(name=f"{prefix}dev insights", value="Sehe alle Insights zu dem Bot!", inline=False)
        embed.add_field(name=f"{prefix}dev togglecommand", value="Sehe alle Insights zu dem Bot!", inline=False)
        embed.add_field(name=f"{prefix}dev userinfo", value="Sehe alle Daten zu einem Nutzer!", inline=False)
        embed.add_field(name=f"{prefix}dev userreset", value="Lösche eine Nutzer-Konfiguration!", inline=False)
        embed.add_field(name=f"{prefix}dev guildinfo", value="Sehe alle Daten zu einer Guild!", inline=False)
        embed.add_field(name=f"{prefix}dev guildreset", value="Lösche eine Guild-Konfiguration!", inline=False)
        embed.add_field(name=f"{prefix}dev log", value="Sehe alle Daten zu einer Guild!", inline=False)
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)

    @dev.command(name="insights", aliases=["dashboard", "stats"])
    @commands.is_owner()
    async def insights(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        embed = discord.Embed(
            title="**[Dev] Insights**",
            description='Klicke auf den folgenden Link, um zu den Statistiken zu gelangen!\n\nhttps://statcord.com/bot/' + str(
                self.bot.user.id) if STATCORD_TOKEN else 'Der Bot ist nicht mit Statcord verknüpft!',
            colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)

    @dev.command(name="togglecommand", aliases=["togglecmd", "cmd", "command"])
    @commands.is_owner()
    async def togglecommand(self, ctx: commands.Context, *, command_in):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        command_in = command_in.lower()
        command = self.bot.get_command(command_in)
        if not command:
            embed = discord.Embed(
                title=f"**Fehler**", description=f"Der Befehl ```{command_in}``` konnte nicht gefunden werden!",
                colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        if command.name == "dev":
            embed = discord.Embed(
                title=f"**Fehler**", description=f"Der Befehl ```{command_in}``` kann nicht deaktiviert werden!",
                colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        command.enabled = not command.enabled
        embed = discord.Embed(
            title="**[Dev] Toggle-Command**",
            description=f"Der Befehl ```{command_in}``` wurde erfolgreich {'aktiviert' if command.enabled else 'deaktiviert'}!",
            colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)

    @dev.command(name="userinfo", aliases=["user", "nutzerinfo"])
    @commands.is_owner()
    async def userinfo(self, ctx: commands.Context, user: discord.User = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
        if not user:
            user = ctx.author
        embed = discord.Embed(
            title=f"**[Dev] Nutzerinfo für {user.name}**",
            colour=await get_embedcolour(ctx.message)
        )
        total, owned = 0, 0
        for guild in self.bot.guilds:
            if user in guild.members:
                total += 1
                if guild.owner == user:
                    owned += 1

        try:
            cmd_usages = await readjson(key=str(user.id),
                                        path=os.path.join("data", "cache", "commandamount_user_cache.json"))
        except KeyError:
            cmd_usages = 0
        embed.add_field(name=f"Name", value=str(user), inline=False)
        embed.add_field(name=f"ID", value=str(user.id), inline=False)
        embed.add_field(name=f"Befehlsnutzungen",
                        value=str(cmd_usages) if cmd_usages != 0 else 'Keine Daten vorhanden!', inline=False)
        embed.add_field(name=f"Guilds mit dem Bot", value=f"Gesamt: {total}\nBesitzer: {owned}", inline=False)
        embed._footer = await get_embed_footer(ctx)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
        path = os.path.join("data", "user", f"{user.id}.json")
        if os.path.isfile(path):
            await ctx.send(file=discord.File(path))

    @dev.command(name="userreset", aliases=["userdelete"])
    @commands.is_owner()
    async def userreset(self, ctx: commands.Context, user: discord.User = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        if not user:
            user = ctx.author
        path = os.path.join("data", "user", f"{user.id}.json")
        if not os.path.isfile(path):
            embed = discord.Embed(
                title=f"**Fehler**", description=f"Der Nutzer **{user}** besitzt keine Settings-Datei!",
                colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        os.remove(path)
        embed = discord.Embed(
            title=f"**[Dev] Settings Reset von {user}**",
            description=f"Die Datei ```{user.id}.json``` wurde gelöscht!",
            colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)

    @dev.command(name="guildinfo", aliases=["guild"])
    @commands.is_owner()
    async def guildinfo(self, ctx: commands.Context, guild: discord.Guild = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
        if not guild:
            guild = ctx.guild
        embed = discord.Embed(
            title=f"**[Dev] Guildinfo für {guild.name}**",
            colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(name=f"Name", value=str(guild.name), inline=False)
        embed.add_field(name=f"ID", value=str(guild.id), inline=False)
        embed.add_field(name=f"Bot auf der Guild?", value='Ja' if self.bot.user in guild.members else 'Nein',
                        inline=False)
        embed._footer = await get_embed_footer(ctx)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)
        path = os.path.join("data", "configs", f"{guild.id}.json")
        if os.path.isfile(path):
            await ctx.send(file=discord.File(path))

    @dev.command(name="configreset", aliases=["configdelete", "guildreset", "guilddelete"])
    @commands.is_owner()
    async def configreset(self, ctx: commands.Context, guild: discord.Guild = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        if not guild:
            guild = ctx.guild
        path = os.path.join("data", "configs", f"{guild.id}.json")
        if not os.path.isfile(path):
            embed = discord.Embed(
                title=f"**Fehler**", description=f"Die Guild **{guild.name}** besitzt keine Config-Datei!",
                colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f"**[Dev] Config Reset von {guild.name}**",
            description=f"Die Datei ```{guild.id}.json``` wurde gelöscht!",
            colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        os.remove(path)
        await ctx.send(embed=embed)

    @dev.group(name="log", aliases=["logs"])
    @commands.is_owner()
    async def log(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.log_help)

    @log.command(name="help", aliases=["hilfe"])
    @commands.is_owner()
    async def log_help(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="**[Dev] Log Hilfe**", description=f"Hier findest du alle Sub-Befehle zum `{prefix}dev log` Befehl!",
            colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(name=f"{prefix}dev log show", value="Schau dir den einer angegebenen Guild an!", inline=False)
        embed.add_field(name=f"{prefix}dev log reset", value="Resette den Log einer spezifischen Guild!", inline=False)
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)

    @log.command(name="show", aliases=["s"])
    @commands.is_owner()
    async def log_show(self, ctx: commands.Context, guild: discord.Guild = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        if not guild:
            guild = ctx.guild
        path = os.path.join("data", "logs", f"{guild.id}.txt")
        if not os.path.isfile(path):
            embed = discord.Embed(
                title=f"**Fehler**", description=f"Die Guild **{guild.name}** besitzt keinen Log!",
                colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title=f"**[Dev] Log von {guild.name}**", description=f"Als Anhang findest du den vollständigen Log!",
            colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await ctx.send(file=discord.File(path))

    @log.command(name="reset", aliases=["r", "delete", "del"], usage="<Guild>")
    @commands.is_owner()
    async def log_reset(self, ctx: commands.Context, guild: discord.Guild = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        if not guild:
            guild = ctx.guild
        path = os.path.join("data", "logs", f"{guild.id}.txt")
        if not os.path.isfile(path):
            embed = discord.Embed(
                title=f"**Fehler**", description=f"Die Datei ```{guild.id}.txt``` konnte nicht gefunden werden!",
                colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            return
        os.remove(path)
        embed = discord.Embed(
            title=f"**[Dev] Log Reset von {guild.name}**",
            description=f"Die Datei ```{guild.id}.txt``` wurde gelöscht!",
            colour=await get_embedcolour(ctx.message)
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)


########################################################################################################################


def setup(bot):
    bot.add_cog(dev(bot))
