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
    Bot,
    NSFWChannelRequired, DisabledCommand,
)

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_errors import check_if_error
from cogs.core.config.config_memechannel import memechannel_check
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.ctx_utils import get_commandname
from cogs.core.functions.func_json import readjson
from cogs.core.functions.logging import log
from config import DISCORD_LINK


class on_command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        commandname = await get_commandname(ctx)
        if commandname in ["meme"]:
            if not await memechannel_check(ctx):
                Bot.dispatch(self.bot, "memechannelcheck_failure", ctx)
                return
        else:
            if not await botchannel_check(ctx):
                Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
                return
        if isinstance(error, CommandNotFound):
            if not await check_if_error(ctx=ctx, error="command_not_found"):
                return
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Befehl `{commandname}` existiert nicht, du kannst alle Befehle mit "
                f"`{await get_prefix_string(ctx.message)}help` sehen!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f'{time}: Der Nutzer {user} hat versucht den nicht existierenden Befehl "{commandname}" auszuführen.',
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, NotOwner):
            if not await check_if_error(ctx=ctx, error="not_owner"):
                return
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
            if not await check_if_error(ctx=ctx, error="bot_missing_permissions"):
                return
            embed = discord.Embed(
                title="**Fehler**",
                description="Mir fehlt folgende Berrechtigung um den Befehl auszuführen:"
                f"```{str(error.missing_perms[0])}```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
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
            if not await check_if_error(ctx=ctx, error="badargument"):
                return
            path = os.path.join("data", "errors", "badargument.json")
            badargument = await readjson(path=path, key=commandname)
            embed = discord.Embed(
                title="**Fehler**",
                description=badargument
                if badargument
                else f"Du hast ein ungültiges Argument angegeben! Nutzung: ```{ctx.command.usage}```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
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
            if not await check_if_error(ctx=ctx, error="command_on_cooldown"):
                return
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
                f"{await get_prefix_string(ctx.message)}{commandname}' im Kanal #{ctx.channel.name} zu nutzen.",
                ctx.guild.id,
            )
            return
        elif isinstance(error, MissingPermissions):
            if not await check_if_error(ctx=ctx, error="user_missing_permissions"):
                return
            embed = discord.Embed(
                title="**Fehler**",
                description="Dir fehlt folgende Berrechtigung um den Befehl auszuführen:"
                f"```{str(error.missing_perms[0])}```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
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
            if not await check_if_error(ctx=ctx, error="missing_argument"):
                return
            commandusage = ctx.command.usage
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Du hast nicht alle erforderlichen Argumente angegeben, Nutzung:```"
                + await get_prefix_string(ctx.message)
                + f"{commandname} {commandusage}```",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
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
        elif isinstance(error, NSFWChannelRequired):
            if not await check_if_error(ctx=ctx, error="not_nsfw_channel"):
                return
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Befehl `{commandname}` kann nur in einem NSFW Kanal ausgeführt "
                f"werden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f'{time}: Der Nutzer {user} hat versucht den NSFW Befehl "{commandname}" in einem normalen Kanal auszuführen.',
                guildid=ctx.guild.id,
            )
            return
        elif isinstance(error, DisabledCommand):
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Der Befehl {commandname} wurde vorübergehend **global deaktiviert**! \n\nKomm auf unseren Support Discord, wenn du mehr Informationen benötigst:\n{DISCORD_LINK}",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f'{time}: Der Nutzer {user} hat versucht den nicht existierenden Befehl "{commandname}" auszuführen.',
                guildid=ctx.guild.id,
            )
            return
        raise error


########################################################################################################################


def setup(bot):
    bot.add_cog(on_command_error(bot))
