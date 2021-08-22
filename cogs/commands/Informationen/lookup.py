import datetime
import discord
import whois
import socket
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, BadArgument

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lookup(self, ctx, domain: str):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            if "http" in domain:
                embed = discord.Embed(
                    title="**Fehler**", colour=get_embedcolour(ctx.message)
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
                    value="Du musst eine Domain ohne http/-s angeben, z.B. ```example.org```",
                    inline=True,
                )
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + get_prefix_string(ctx.message)
                    + "lookup angegeben.",
                    guildid=ctx.guild.id,
                )
                return
            w = whois.whois(domain)
            if w.domain_name is None:
                embed = discord.Embed(
                    title="**Fehler**", colour=get_embedcolour(ctx.message)
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
                    value="Du musst eine existierende Domain angeben, z.B. ```example.org```",
                    inline=True,
                )
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + get_prefix_string(ctx.message)
                    + "lookup angegeben.",
                    guildid=ctx.guild.id,
                )
                return

            def get_ip():
                try:
                    ip = socket.gethostbyname(domain)
                except Exception:
                    ip = "failed"
                return ip

            embed = discord.Embed(
                title=f"**Informationen zur Domain {domain}**",
                colour=get_embedcolour(ctx.message),
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.add_field(name="**Domain:**", value=w.domain_name, inline=True)
            embed.add_field(name="**Registrar:**", value=w.registrar, inline=True)
            embed.add_field(name="**IP:**", value=get_ip(), inline=True)
            embed.add_field(
                name="**Standort:**", value=f"{w.state} / {w.country}", inline=True
            )
            embed.add_field(
                name="**Buchungsdatum:**", value=w.creation_date, inline=True
            )
            embed.add_field(
                name="**Auslaufdatum:**", value=w.expiration_date, inline=True
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
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "meme benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "lookup im Channel #"
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

    @lookup.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
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
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "lookup <Domain>```"
                "`Hinweis: Bitte ohne http/-s angeben, also z.B. communitybot.visitlink.de`",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "lookup eingegeben.",
                guildid=ctx.guild.id,
            )
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
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
                value="Du musst eine richtige Domain angeben, z.B. ```communitybot.visitlink.de```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat ein ungültiges Argument bei "
                + get_prefix_string(ctx.message)
                + "lookup angegeben.",
                guildid=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(lookup(bot))
