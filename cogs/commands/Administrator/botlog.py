import datetime
import os
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log


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
        path = os.path.join("data", "logs", f"{ctx.guild.id}.txt")
        if await botchannel_check(ctx):
            try:
                if os.path.isfile(path):
                    await log(
                        text=str(time)
                        + ": Der Nutzer "
                        + str(user)
                        + ' hat sich den Log mit der ID "'
                        + str(ctx.guild.id)
                        + '" ausgeben lassen!',
                        guildid=ctx.guild.id,
                    )
                    await msg2.add_reaction(emoji="✅")
                    await ctx.author.send(file=discord.File(path))
                    embed = discord.Embed(
                        title="**Erfolgreich**",
                        description="Schau in deine Privatnachrichten!",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="**Fehler**", colour=await get_embedcolour(ctx.message)
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    embed.add_field(
                        name="‎",
                        value="Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster "
                        "Befehl ist!",
                        inline=False,
                    )
                    await ctx.send(embed=embed)
                    await log(
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
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(botlog(bot))
