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


class join(commands.Cog):
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

    async def connect_to_player(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        player = ctx.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)
        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)

    @commands.command(
        name="join",
    )
    async def join(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        player = ctx.bot.wavelink.get_player(ctx.guild.id)
        if await botchannel_check(ctx):
            if not ctx.author.voice:
                embed = discord.Embed(
                    title="Fehler",
                    description=f"Du befindest dich in keinem Sprachkanal!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                    "join zu benutzen, befand sich aber in keinem Sprachkanal!",
                    guildid=ctx.guild.id,
                )
                return
            await self.connect_to_player(ctx)
            embed = discord.Embed(
                title="Musik Join",
                description="Ich bin erfolgreich deinem Sprachkanal beigetreten!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                "join benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(join(bot))
