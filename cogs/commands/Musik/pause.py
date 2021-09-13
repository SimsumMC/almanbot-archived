import datetime

import discord
import wavelink
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from config import lavalink


class pause(commands.Cog):
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

    @commands.command(name="pause")
    async def pause(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler",
                description="Du befindest dich in keinem Sprachkanal!",
                colour=get_embedcolour(ctx.message),
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                "pause zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        await ctx.bot.wavelink.get_player(ctx.guild.id).set_pause(True)
        embed = discord.Embed(
            title="Musik Pause",
            description="Ich habe erfolgreich die Musik pausiert!",
            colour=get_embedcolour(ctx.message),
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
            "pause benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################

def setup(bot):
    bot.add_cog(pause(bot))
