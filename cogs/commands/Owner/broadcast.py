import datetime
import traceback

import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL, DEFAULT_BROADCAST_MESSAGE


class broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="broadcast", aliases=["ankündigung", "ownermsg", "rundruf"])
    @commands.is_owner()
    async def broadcast(self, ctx, *, message):
        user = ctx.author
        time = datetime.datetime.now()
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Broadcast**",
                description=DEFAULT_BROADCAST_MESSAGE + "\n\n" + str(message),
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            aldready_messaged = []
            failed = []
            for guild in self.bot.guilds:
                owner = guild.owner
                if owner.id in aldready_messaged:
                    continue
                try:
                    await owner.send(embed=embed)
                except Exception:
                    failed.append(owner.id)
                aldready_messaged.append(owner.id)
            embed2 = discord.Embed(
                title="**Broadcast**",
                description="Erfolgreich versendet!",
                colour=get_embedcolour(message=ctx.message),
            )
            if failed:
                embed2.add_field(name="Fehler", value="".join([id for id in failed]))
            embed2.set_thumbnail(url=THUMBNAIL_URL)
            embed2.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            try:
                await ctx.send(embed=embed2)
            except Exception:
                traceback.print_exc()
        else:
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_footer(
                text=get_embed_footer_text(ctx),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value="Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster "
                "Befehl ist!",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + ' hat sich probiert den noch nicht existierenden Log mit der ID "'
                + str(ctx.guild.id)
                + '" ausgeben zu lassen!',
                guildid=ctx.guild.id,
            )


###############################################################################################################


def setup(bot):
    bot.add_cog(broadcast(bot))
