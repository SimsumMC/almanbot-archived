import datetime

import discord
import wavelink
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from config import lavalink


class leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        try:
            await self.bot.wavelink.initiate_node(
                host=lavalink.host,
                port=lavalink.port,
                rest_uri=lavalink.rest_uri,
                password=lavalink.passwort,
                identifier=lavalink.identifier,
                region=lavalink.region,
            )
        except Exception:
            pass

    @commands.command(name="leave")
    async def leave(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        player = ctx.bot.wavelink.get_player(ctx.guild.id)
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler",
                description="Du befindest dich in keinem Sprachkanal!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "leave zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        elif not ctx.author.voice.channel.id == player.channel_id:
            embed = discord.Embed(
                title="Fehler",
                description="Du befindest dich nicht im dem Sprachkanal, in dem der Bot sich aktuell aufhält!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "leave zu benutzen, befand sich aber nicht in dem gleichen Sprachkanal wie der Bot!",
                guildid=ctx.guild.id,
            )
            return
        await player.destroy()
        embed = discord.Embed(
            title="Musik Stop",
            description="Ich habe erfolgreich deinen Sprachkanal verlassen!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "leave benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(leave(bot))
