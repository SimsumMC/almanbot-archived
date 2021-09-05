import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_trigger import (
    get_trigger_list,
    add_trigger,
    remove_trigger,
)
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class trigger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def trigger(self, ctx):
        if ctx.invoked_subcommand is None:  # todo help
            ...

    @trigger.command(name="add", usage="<Trigger Name : Antwort Nachricht>")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *, input):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx=ctx):
            word = input.split(" : ")[0]
            msg = input.split(" : ")[1]
            if word in get_trigger_list(guildid=ctx.guild.id):
                embed = discord.Embed(
                    title=f"**Fehler**",
                    description=f"Der Trigger {word} existiert bereits! Wenn du ihn verändern möchtest, "
                    f"nutze den Befehl:"
                    f"```{get_prefix_string(message=ctx.message)}trigger edit",
                    colour=get_embedcolour(ctx.message),
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                    f"trigger add zu benutzen und damit den Trigger {word} hinzuzufügen, konnte"
                    f" es aber nicht da dieser bereits existiert hat!",
                    guildid=ctx.guild.id,
                )
                return
            add_trigger(guildid=ctx.guild.id, trigger=word, msg=msg)
            embed = discord.Embed(
                title=f"**Trigger Add**",
                description=f"Der Bot reagiert nun auf ```{word}``` mit der Nachricht:"
                f"```{msg}```",
                colour=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                f"trigger add benutzt und damit den Trigger {word} hinzugefügt.!",
                guildid=ctx.guild.id,
            )

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @trigger.command(name="remove", usage="<Trigger Name>")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, *, word):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            if trigger in get_trigger_list(guildid=ctx.guild.id):
                embed = discord.Embed(
                    title=f"**Fehler**",
                    description=f"Der Trigger {word} existiert nicht! Wenn du einen erstellen möchtest,"
                    "nutz den Befehl:"
                    f"```{get_prefix_string(message=ctx.message)}trigger add <Name> : <```",
                    colour=get_embedcolour(ctx.message),
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)  # todo add components
                log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                    f"trigger remove zu benutzen und damit den Trigger {word} zu löschen, konnte"
                    f" es aber nicht da dieser nicht existiert hat!",
                    guildid=ctx.guild.id,
                )
                return
            remove_trigger(guildid=ctx.guild.id, trigger=word)
            embed = discord.Embed(
                title=f"**Trigger Remove**",
                description=f"Der Trigger {word}",
                colour=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                f"trigger add benutzt und damit den Trigger {word} hinzugefügt.!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(trigger(bot))
