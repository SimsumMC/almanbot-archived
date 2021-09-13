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


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        await self.bot.wavelink.initiate_node(
            host=lavalink.host,
            port=lavalink.port,
            rest_uri=lavalink.rest_uri,
            password=lavalink.passwort,
            identifier=lavalink.identifier,
            region=lavalink.region,
        )

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
        if botchannel_check(ctx):
            if not ctx.author.voice:
                embed = discord.Embed(
                    title="Fehler", description="Du befindest dich in keinem Sprachkanal!",
                    colour=get_embedcolour(ctx.message)
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                    "join zu benutzen, befand sich aber in keinem Sprachkanal!",
                    guildid=ctx.guild.id,
                )
                return
            await self.connect_to_player(ctx)
            embed = discord.Embed(
                title="Musik Join", description="Ich bin erfolgreich deinem Sprachkanal beigetreten!",
                colour=get_embedcolour(ctx.message)
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "join benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @commands.command(name="play", usage="<Name vom Song / YT Link>")
    async def play(self, ctx: commands.Context, *, query):
        time = datetime.datetime.now()
        user = ctx.author.name
        if botchannel_check(ctx):
            tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")
            if not tracks:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=f"Ich konnte keinen Song mit der Suchanfrage ````{query}``` finden!",
                    colour=get_embedcolour(message=ctx.message),
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
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
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_thumbnail(
                url="https://img.youtube.com/vi/" + tracks[0].info["uri"].split("=")[1] + "/default.jpg"
            )
            embed.add_field(name="**Name**", value=tracks[0].info["title"])
            embed.add_field(name="**Author**", value=tracks[0].info["author"])
            embed.add_field(
                name="**Länge**",
                value=str(datetime.timedelta(milliseconds=tracks[0].info["length"]))
                      + "h",
            )
            embed._footer = get_embed_footer(ctx)
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
            log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                f"play benutzt und damit den Song "
                + str(tracks[0].info["title"])
                + " abgespielt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)

    @commands.command(name="stop")
    async def stop(self, ctx):  # TODO
        time = datetime.datetime.now()
        user = ctx.author.name
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler", description="Du befindest dich in keinem Sprachkanal!", colour=get_embedcolour(ctx.message)
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                "stop zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        await ctx.bot.wavelink.get_player(ctx.guild.id).stop()
        embed = discord.Embed(
            title="Musik Stop", description="Ich habe erfolgreich die Musik gestoppt!",
            colour=get_embedcolour(ctx.message)
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
            "stop benutzt!",
            guildid=ctx.guild.id,
        )

    @commands.command(name="leave")
    async def leave(self, ctx):  # TODO
        time = datetime.datetime.now()
        user = ctx.author.name
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler", description="Du befindest dich in keinem Sprachkanal!",
                colour=get_embedcolour(ctx.message)
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                "leave zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        await ctx.bot.wavelink.get_player(ctx.guild.id).destroy()
        embed = discord.Embed(
            title="Musik Stop", description="Ich habe erfolgreich deinen Sprachkanal verlassen!",
            colour=get_embedcolour(ctx.message)
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
            "leave benutzt!",
            guildid=ctx.guild.id,
        )

    @commands.command(name="volume", aliases=["vol", "lautstärke"], usage="<Lautstärke von 1-100>")
    @commands.has_permissions(administrator=True)
    async def volume(self, ctx, volume: int):
        time = datetime.datetime.now()
        user = ctx.author.name
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler", description="Du befindest dich in keinem Sprachkanal!",
                colour=get_embedcolour(ctx.message)
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                "volume zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        if not volume > 0 or not volume < 1000:
            embed = discord.Embed(
                title="Fehler", description="Du musst eine ganze Zahl von ```0 - 1000``` angeben!",
                colour=get_embedcolour(ctx.message)
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                "volume zu benutzen, die eingebene Lautstärke war aber zu hoch!",
                guildid=ctx.guild.id,
            )
            return
        await ctx.bot.wavelink.get_player(ctx.guild.id).set_volume(volume)
        embed = discord.Embed(
            title="Musik Lautstärke", description=f"Ich habe die Lautstärke auf {volume} gesetzt!",
            colour=get_embedcolour(ctx.message)
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat mit den Befehl {get_prefix_string(ctx.message)}"
            f"volume die Lautstärke auf {volume} gesetzt!",
            guildid=ctx.guild.id,
        )

    @commands.command(name="leave") #
    async def leave(self, ctx):  # TODO
        time = datetime.datetime.now()
        user = ctx.author.name
        if not ctx.author.voice:
            embed = discord.Embed(
                title="Fehler", description="Du befindest dich in keinem Sprachkanal!",
                colour=get_embedcolour(ctx.message)
            )
            embed._footer = get_embed_footer(ctx)
            embed._thumbnail = get_embed_thumbnail()
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Nutzer {user} hat versucht den Befehl {get_prefix_string(ctx.message)}"
                "leave zu benutzen, befand sich aber in keinem Sprachkanal!",
                guildid=ctx.guild.id,
            )
            return
        await ctx.bot.wavelink.get_player(ctx.guild.id).pause()
        embed = discord.Embed(
            title="Musik Pause", description="Ich habe erfolgreich die Musik pausiert!",
            colour=get_embedcolour(ctx.message)
        )
        embed._footer = get_embed_footer(ctx)
        embed._thumbnail = get_embed_thumbnail()
        await ctx.send(embed=embed)
        log(
            f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
            "leave benutzt!",
            guildid=ctx.guild.id,
        )
########################################################################################################################


def setup(bot):
    bot.add_cog(music(bot))
