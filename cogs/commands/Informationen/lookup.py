import datetime
import socket

import discord
import whois
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


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
        if await botchannel_check(ctx):
            if "http" in domain:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Du musst eine Domain ohne http/-s angeben, z.B. ```example.org```",
                    inline=True,
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Nutzer "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + await get_prefix_string(ctx.message)
                    + "lookup angegeben.",
                    guildid=ctx.guild.id,
                )
                return
            w = whois.whois(domain)
            if w.domain_name is None:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Du musst eine existierende Domain angeben, z.B. ```example.org```",
                    inline=True,
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Nutzer "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + await get_prefix_string(ctx.message)
                    + "lookup angegeben.",
                    guildid=ctx.guild.id,
                )
                return

            async def get_ip():
                try:
                    ip = socket.gethostbyname(domain)
                except Exception:
                    ip = "failed"
                return ip

            embed = discord.Embed(
                title=f"**Informationen zur Domain {domain}**",
                colour=await get_embedcolour(ctx.message),
            )
            embed.add_field(name="**Domain:**", value=w.domain_name, inline=True)
            embed.add_field(
                name="**Registrar:**",
                value=w.registrar if not "null" else "-",
                inline=True,
            )
            embed.add_field(name="**IP:**", value=await get_ip(), inline=True)
            embed.add_field(
                name="**Standort:**",
                value=f"{w.state} / {w.country}" if not "null" else "-",
                inline=True,
            )
            embed.add_field(
                name="**Buchungsdatum:**",
                value=w.creation_date if not "null" else "-",
                inline=True,
            )
            embed.add_field(
                name="**Auslaufdatum:**",
                value=w.expiration_date if not "null" else "-",
                inline=True,
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + await get_prefix_string(ctx.message)
                + "meme benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(lookup(bot))
