import datetime
import socket

import discord
import whois
from discord.ext import commands

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL, WRONG_CHANNEL_ERROR


class lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="lookup",
        aliases=["whois", "domaininfo"],
        usage="<Domain>",
    )
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
                    text=get_embed_footer_text(ctx),
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
                    + ": Der Nutzer "
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
                    text=get_embed_footer_text(ctx),
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
                    + ": Der Nutzer "
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
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "meme benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            log(
                text=str(time)
                + ": Der Nutzer "
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
                text=get_embed_footer_text(ctx),
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
    bot.add_cog(lookup(bot))
