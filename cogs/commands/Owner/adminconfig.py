import os
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import (
    get_embedcolour,
    get_embedcolour_code,
    embedcolour_check,
)
from cogs.core.config.config_memes import get_memes, redditnsfwcheck, meme_is_checked
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import writejson, readjson


class adminconfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        usage="<Guild ID> <Modul> <Wert>"
    )  # todo adminconfig als group with reset, show and edit
    @commands.is_owner()
    async def adminconfig(self, ctx, guildid, subcommand, arg):
        path = os.path.join("data", "configs", f"{guildid}.json")
        existing = [
            "prefix",
            "botchannel",
            "memechannel",
            "memesource",
            "colour",
            "hilfe",
        ]
        if botchannel_check(ctx):
            if subcommand in existing:
                if subcommand == "colour":
                    if embedcolour_check(arg) is True:
                        writejson(
                            type=subcommand,
                            input=get_embedcolour_code(str(arg)),
                            path=path,
                        )
                        embed = discord.Embed(
                            title="**Admin Config**",
                            description="Das Modul ```"
                            + str(subcommand)
                            + "``` wurde erfolgreich zu ```"
                            + str(arg)
                            + "``` geändert!",
                            colour=get_embedcolour(ctx.message),
                        )
                        embed._footer = get_embed_footer(ctx)
                        embed._thumbnail = get_embed_thumbnail()
                        await ctx.send(embed=embed)
                        return
                    else:
                        embed = discord.Embed(
                            title="**Fehler**",
                            description="Das Modul ```"
                            + str(subcommand)
                            + "``` kann nicht zu ```"
                            + str(arg)
                            + "``` geändert werden.",
                            colour=get_embedcolour(ctx.message),
                        )
                        embed._footer = get_embed_footer(ctx)
                        embed._thumbnail = get_embed_thumbnail()
                        await ctx.send(embed=embed)
                        return

                elif subcommand == "memesource":
                    path2 = os.path.join("data", "verifiedmemes", "memes.json")
                    if arg == "default":
                        arg = "memes"
                    if arg != get_memes(guildid) and meme_is_checked(arg) is False:
                        if arg in readjson("failed", path2) or redditnsfwcheck(arg):
                            embed = discord.Embed(
                                title="**Fehler**",
                                description=f"Der angegebene Reddit **{arg}** enthält nicht "
                                "zulässigen Inhalt.",
                                color=get_embedcolour(ctx.message),
                            )
                            embed._footer = get_embed_footer(ctx)
                            embed._thumbnail = get_embed_thumbnail()
                            await ctx.send(embed=embed)
                            return
                writejson(type=subcommand, input=arg, path=path)
                embed = discord.Embed(
                    title="**Admin Config**", colour=get_embedcolour(ctx.message)
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Das Modul ```"
                    + str(subcommand)
                    + "``` wurde erfolgreich zu ```"
                    + str(arg)
                    + "``` geändert!",
                    inline=False,
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="**Fehler**", colour=get_embedcolour(ctx.message)
                )
                embed._footer = get_embed_footer(ctx)
                embed._thumbnail = get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Das Modul **" + str(subcommand) + "** existiert nicht!",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(adminconfig(bot))
