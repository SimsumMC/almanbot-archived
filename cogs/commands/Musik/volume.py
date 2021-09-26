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


class volume(commands.Cog):
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

    @commands.command(
        name="volume", aliases=["vol", "lautstärke"], usage="<Lautstärke von 1-1000>"
    )
    @commands.has_permissions(administrator=True)
    async def volume(self, ctx, volume: int):
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
                "volume zu benutzen, befand sich aber in keinem Sprachkanal!",
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
                "volume zu benutzen, befand sich aber nicht in dem gleichen Sprachkanal wie der Bot!",
                guildid=ctx.guild.id,
            )
            return
        elif not player.is_connected or not player.is_playing:
            embed = discord.Embed(
                title="Fehler",
                description="Der Bot spielt keine Musik und kann daher die Lautstärke !",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "volume zu benutzen, es wurde aber kein Song abgespielt!",
                guildid=ctx.guild.id,
            )
            return
        elif not volume >= 0 or not volume <= 1000:
            embed = discord.Embed(
                title="Fehler",
                description="Du musst eine ganze Zahl von ```0 - 1000``` angeben!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                "volume zu benutzen, die eingebene Lautstärke war aber zu hoch!",
                guildid=ctx.guild.id,
            )
            return
        await player.set_volume(volume)
        embed = discord.Embed(
            title="Musik Lautstärke",
            description=f"Ich habe die Lautstärke auf {volume} gesetzt!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat mit den Befehl {await get_prefix_string(ctx.message)}"
            f"volume die Lautstärke auf {volume} gesetzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(volume(bot))
