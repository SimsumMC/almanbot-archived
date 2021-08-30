import datetime
import os
import traceback

import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL, WRONG_CHANNEL_ERROR


class botlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="botlog",
        aliases=["serverlog", "log"],
        description="Gebe dir den Botlog deines Servers aus!",
    )
    @commands.has_permissions(view_audit_log=True)
    async def botlog(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join("data", "logs", f"{ctx.guild.id}.txt")
        if botchannel_check(ctx):
            try:
                if os.path.isfile(path):
                    log(
                        text=str(time)
                        + ": Der Nutzer "
                        + str(user)
                        + ' hat sich den Log mit der ID "'
                        + str(ctx.guild.id)
                        + '" ausgeben lassen!',
                        guildid=ctx.guild.id,
                    )
                    await msg2.add_reaction(emoji="✅")
                    await ctx.author.send(
                        content="test",
                        file=discord.File(path, filename="log.txt")
                        # todo doesnt work
                    )  # todo missing error handling here wenn author has dms blocked
                    embed = discord.Embed(
                        title="**Erfolgreich**",
                        description="Schau in deine Privatnachrichten!",
                        colour=get_embedcolour(ctx.message),
                    )
                    embed.set_thumbnail(url=THUMBNAIL_URL)
                    embed.set_footer(
                        text=get_embed_footer_text(ctx),
                        icon_url=ICON_URL,
                    )
                    await ctx.send(embed=embed)
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
                        + ' hat versucht sich den noch nicht existierenden Log mit der ID "'
                        + str(ctx.guild.id)
                        + '" ausgeben zu lassen!',
                        guildid=ctx.guild.id,
                    )
            except Exception:
                traceback.print_exc()

        else:
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "serverlog im Channel #"
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
    bot.add_cog(botlog(bot))
