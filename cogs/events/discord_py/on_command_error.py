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
)

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_errors import check_if_error
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.func_json import readjson
from cogs.core.functions.logging import log
from config import (
    ICON_URL,
    THUMBNAIL_URL,
    WRONG_CHANNEL_ERROR,
    WRONG_CHANNEL_ERROR_DELETE_AFTER,
)


def get_commandname(ctx):
    if not ctx.command:
        return ctx.message.content.split(" ")[0]
    elif ctx.invoked_subcommand:
        parents = ""
        for p in ctx.invoked_parents:
            parents = parents + p + " "
        else:
            parents = parents[:-1]
        commandname = str(parents) + " " + str(ctx.invoked_subcommand.name)
    else:
        commandname = ctx.command.name
    return commandname


class on_command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        msg2 = ctx.message
        name = ctx.channel.name
        commandname = get_commandname(ctx)
        if not botchannel_check(
            ctx
        ):  # todo with event ( on_botchannel_check_failure? )
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + f"{commandname} im Channel #"
                + str(name)
                + " zu benutzen!",
                guildid=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed, delete_after=WRONG_CHANNEL_ERROR_DELETE_AFTER)
            await msg2.delete()
            return
        elif isinstance(error, CommandNotFound):
            if not check_if_error(ctx=ctx, error="commandnotfound"):
                return
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=f"Der Befehl `{commandname}` existiert nicht, du kannst alle Befehle mit "
                f"`{get_prefix_string(ctx.message)}help` sehen!",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                f'{time}: Der Nutzer {user} hat versucht den nicht existierenden Befehl "{commandname}" auszuführen.',
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, NotOwner):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value="Du musst der Besitzer sein, um diesen Befehl nutzen zu dürfen!",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um den Befehl "
                + get_prefix_string(ctx.message)
                + f"{commandname} zu nutzen.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, BotMissingPermissions):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value="Mir fehlt folgende Berrechtigung um den Befehl auszuführen:"
                f"```{str(error.missing_perms[0])}```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Bot hatte nicht die nötigen Berrechtigungen um den Befehl"
                + get_prefix_string(ctx.message)
                + f"{commandname} vom Nutzer {user} auszuführen.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, BadArgument):
            path = os.path.join("data", "errors", "badargument.json")
            badargument = readjson(path=path, key=commandname)
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=badargument,
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat ein ungültiges Argument bei "
                + get_prefix_string(ctx.message)
                + f"{commandname} angegeben.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, CommandOnCooldown):
            embed = discord.Embed(
                title="**Cooldown**",
                description=f"Versuch es nochmal in {error.retry_after:.2f}s.",
                color=get_embedcolour(ctx.message),
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat trotz eines Cooldowns versucht den Befehl '"
                f"{get_prefix_string(ctx.message)}{commandname}' im Kanal #{ctx.channel.name} zu nutzen.",
                ctx.guild.id,
            )
            return
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value="Dir fehlt folgende Berrechtigung um den Befehl auszuführen:"
                f"```{str(error.missing_perms[0])}```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um den Befehl"
                + get_prefix_string(ctx.message)
                + f"{commandname} zu nutzen.",
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, MissingRequiredArgument):
            commandusage = ctx.command.usage
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung:```"
                + get_prefix_string(ctx.message)
                + f"{commandname} {commandusage}```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + f"{commandname} eingegeben.",
                guildid=ctx.guild.id,
            )
            return
        raise error


########################################################################################################################


def setup(bot):
    bot.add_cog(on_command_error(bot))
