import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
from discord_components import Button

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_trigger import (
    get_trigger_list,
    add_trigger,
    remove_trigger,
)
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import WRONG_CHANNEL_ERROR

from config import ICON_URL, THUMBNAIL_URL, FOOTER


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
        try:
            print(trigger.add.usage)
        except Exception:
            pass
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        prefix = get_prefix_string(message=ctx.message)
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
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(text=get_embed_footer_text(ctx), icon_url=ICON_URL)
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                f"trigger add benutzt und damit den Trigger {word} hinzugefügt.!",
                guildid=ctx.guild.id,
            )

        else:
            log(
                text=f"{time}: Der Nutzer {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                     f"trigger add im Channel #{name} zu benutzen!",
                guildid=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_footer(text=get_embed_footer_text(ctx), icon_url=ICON_URL)
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()

    @trigger.command(name="remove", usage="<Trigger Name>")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, *, word):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            if trigger in get_trigger_list(guildid=ctx.guild.id):
                embed = discord.Embed(
                    title=f"**Fehler**",
                    description=f"Der Trigger {word} existiert nicht! Wenn du einen erstellen möchtest,"
                                "nutz den Befehl:"
                                f"```{get_prefix_string(message=ctx.message)}trigger add <Name> : <```",
                    colour=get_embedcolour(ctx.message),
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.set_footer(
                    text=get_embed_footer_text(ctx),
                    icon_url=ICON_URL,
                )
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
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text="for "
                     + str(user)
                     + " | by "
                     + str(get_author())
                     + " | Prefix "
                     + get_prefix_string(message=ctx.message),
                icon_url="https://media.discordapp.net/attachments/645276319311200286"
                         "/803322491480178739/winging-easy.png?width=676&height=676",
            )
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                f"trigger add benutzt und damit den Trigger {word} hinzugefügt.!",
                guildid=ctx.guild.id,
            )
        else:
            log(
                text=f"{time}: Der Nutzer {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                     f"trigger add im Channel #{name} zu benutzen!",
                guildid=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
            )
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
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(trigger(bot))
