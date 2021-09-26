import datetime

import discord
import wavelink
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, ButtonStyle

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from config import lavalink


class play(commands.Cog):
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

    @commands.command(name="play", usage="<Name vom Song / YT Link>")
    async def play(self, ctx: commands.Context, *, query):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
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
                    "play zu benutzen, befand sich aber in keinem Sprachkanal!",
                    guildid=ctx.guild.id,
                )
                return

            tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")
            if not tracks:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=f"Ich konnte keinen Song mit der Suchanfrage ````{query}``` finden!",
                    colour=await get_embedcolour(message=ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}"
                    f"play zu benutzen und damit den Song "
                    + tracks[0].info["title"]
                    + " abzuspielen,"
                    f" der konnte aber nicht gefunden werden!",
                    guildid=ctx.guild.id,
                )
                return
            player = self.bot.wavelink.get_player(ctx.guild.id)
            if not player.is_connected:
                await self.connect_to_player(ctx)
            embed = discord.Embed(
                title="**Musik Play**",
                colour=await get_embedcolour(message=ctx.message),
            )
            embed.set_thumbnail(
                url="https://img.youtube.com/vi/"
                + tracks[0].info["uri"].split("=")[1]
                + "/default.jpg"
            )
            embed.add_field(name="**Name**", value=tracks[0].info["title"])
            embed.add_field(name="**Author**", value=tracks[0].info["author"])
            embed.add_field(
                name="**Länge**",
                value=str(datetime.timedelta(milliseconds=tracks[0].info["length"]))
                + "h",
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(
                embed=embed,
                components=[
                    Button(
                        label="YouTube Link",
                        url=str(tracks[0].info["uri"]),
                        style=ButtonStyle.URL,
                    )
                ],
            )
            await player.play(tracks[0])
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                f"play benutzt und damit den Song "
                + str(tracks[0].info["title"])
                + " abgespielt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(play(bot))
