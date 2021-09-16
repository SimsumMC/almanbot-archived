import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import (
    CommandNotFound,
    MissingRequiredArgument,
    CommandOnCooldown,
    BotMissingPermissions,
    NotOwner,
    BadArgument,
    MissingPermissions,
    Bot, )

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_errors import check_if_error
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.ctx_utils import get_commandname
from cogs.core.functions.func_json import readjson
from cogs.core.functions.logging import log


class on_command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        commandname = await get_commandname(ctx)
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        elif isinstance(error, CommandNotFound):
            if not check_if_error(ctx=ctx, error="commandnotfound"):
                return
            embed = discord.Embed(
                title="**Fehler**", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(
                name="‎",
                value=f"Der Befehl `{commandname}` existiert nicht, du kannst alle Befehle mit "
                f"`{await get_prefix_string(ctx.message)}help` sehen!",
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                f'{time}: Der Nutzer {user} hat versucht den nicht existierenden Befehl "{commandname}" auszuführen.',
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, NotOwner):
            embed = discord.Embed(
                title="**Fehler**", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(
                name="‎",
                value="Du musst der Besitzer sein, um diesen Befehl nutzen zu dürfen!",
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um den Befehl "
                + await get_prefix_string(ctx.message)
                + f"{commandname} zu nutzen.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, BotMissingPermissions):
            embed = discord.Embed(
                title="**Fehler**", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(
                name="‎",
                value="Mir fehlt folgende Berrechtigung um den Befehl auszuführen:"
                f"```{str(error.missing_perms[0])}```",
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                text=str(time)
                + ": Der Bot hatte nicht die nötigen Berrechtigungen um den Befehl"
                + await get_prefix_string(ctx.message)
                + f"{commandname} vom Nutzer {user} auszuführen.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, BadArgument):
            path = os.path.join("data", "errors", "badargument.json")
            badargument = await readjson(path=path, key=commandname)
            embed = discord.Embed(
                title="**Fehler**", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(
                name="‎",
                value=badargument,
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat ein ungültiges Argument bei "
                + await get_prefix_string(ctx.message)
                + f"{commandname} angegeben.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, CommandOnCooldown):
            embed = discord.Embed(
                title="**Cooldown**",
                description=f"Versuch es nochmal in {error.retry_after:.2f}s.",
                color=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat trotz eines Cooldowns versucht den Befehl '"
                f"{get_prefix_string(ctx.message)}{commandname}' im Kanal #{ctx.channel.name} zu nutzen.",
                ctx.guild.id,
            )
            return
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="**Fehler**", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(
                name="‎",
                value="Dir fehlt folgende Berrechtigung um den Befehl auszuführen:"
                f"```{str(error.missing_perms[0])}```",
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um den Befehl"
                + await get_prefix_string(ctx.message)
                + f"{commandname} zu nutzen.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, MissingRequiredArgument):
            commandusage = ctx.command.usage
            embed = discord.Embed(
                title="**Fehler**", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            embed.add_field(
                name="‎",
                value=f"Du hast nicht alle erforderlichen Argumente angegeben, Nutzung:```"
                + await get_prefix_string(ctx.message)
                + f"{commandname} {commandusage}```",
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + await get_prefix_string(ctx.message)
                + f"{commandname} eingegeben.",
                guildid=ctx.guild.id,
            )
            return
        raise error


########################################################################################################################


def setup(bot):
    bot.add_cog(on_command_error(bot))
