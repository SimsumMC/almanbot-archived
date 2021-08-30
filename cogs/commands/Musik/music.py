import datetime

import discord
import wavelink
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.logging import log
from config import ICON_URL, WRONG_CHANNEL_ERROR, THUMBNAIL_URL, lavalink


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

    @commands.command(
        name="join",
    )
    async def join(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                player = self.bot.wavelink.get_player(ctx.guild.id)
                await player.connect(channel.id)
                await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
                embed = discord.Embed(
                    title="Musik Join", colour=get_embedcolour(ctx.message)
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.add_field(
                    name="‎",
                    value="Ich bin erfolgreich deinem Voicechannel beigetreten!",
                    inline=False,
                )
                embed.set_footer(
                    text=get_embed_footer_text(ctx),
                    icon_url=ICON_URL,
                )
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                    "join benutzt!",
                    guildid=ctx.guild.id,
                )
            else:
                embed = discord.Embed(
                    title="Fehler",
                    description="Du befindest dich in keinem Voicechannel!",
                    colour=get_embedcolour(ctx.message),
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.set_footer(
                    text=get_embed_footer_text(ctx),
                    icon_url=ICON_URL,
                )
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                    "join benutzt!",
                    guildid=ctx.guild.id,
                )
        else:
            log(
                text=f"{time}: Der Nutzer {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                f"example im Channel #{name} zu benutzen!",
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

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")
        if not tracks:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Ich konnte keinen Song mit der Suchanfrage ````{query}``` finden!",
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            await ctx.send(embed=embed)
            return
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.join)
        print(tracks[0].info)
        print(tracks[0].info["uri"])
        embed = discord.Embed(
            title="**Musik Play**",
            colour=get_embedcolour(message=ctx.message),
        )
        embed.set_thumbnail(
            url="https://img.youtube.com/vi/"
            + tracks[0].info["uri"].split("=")[1]
            + "/default.jpg"
        )
        embed.url = str(tracks[0].info["uri"])
        embed.add_field(name="**Name**", value=tracks[0].info["title"])
        embed.add_field(name="**Author**", value=tracks[0].info["author"])
        embed.add_field(
            name="**Länge**",
            value=str(datetime.timedelta(milliseconds=tracks[0].info["length"])) + "h",
        )
        print(str(datetime.timedelta(seconds=tracks[0].info["length"])))
        embed.set_footer(
            text=get_embed_footer_text(ctx),
            icon_url=ICON_URL,
        )
        await ctx.send(embed=embed)
        await player.play(tracks[0])


########################################################################################################################


def setup(bot):
    bot.add_cog(music(bot))
