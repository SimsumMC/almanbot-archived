import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.func_json import writejson, readjson
from cogs.core.config.config_memes import get_memes, redditnsfwcheck, meme_is_checked
from cogs.core.config.config_embedcolour import (
    get_embedcolour,
    get_embedcolour_code,
    embedcolour_check,
)


class adminconfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # todo adminconfig als group with reset, show and edit
    @commands.is_owner()
    async def adminconfig(self, ctx, guildid, subcommand, arg):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
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
                        embed.set_footer(
                            text=FOOTER[0]
                            + str(user)
                            + FOOTER[1]
                            + str(get_author())
                            + FOOTER[2]
                            + str(get_prefix_string(ctx.message)),
                            icon_url=ICON_URL,
                        )
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
                        embed.set_footer(
                            text=FOOTER[0]
                            + str(user)
                            + FOOTER[1]
                            + str(get_author())
                            + FOOTER[2]
                            + str(get_prefix_string(ctx.message)),
                            icon_url=ICON_URL,
                        )
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
                            embed.set_thumbnail(url=THUMBNAIL_URL)
                            embed.set_footer(
                                text=FOOTER[0]
                                + str(user)
                                + FOOTER[1]
                                + str(get_author())
                                + FOOTER[2]
                                + str(get_prefix_string(ctx.message)),
                                icon_url=ICON_URL,
                            )
                            await ctx.send(embed=embed)
                            return
                writejson(type=subcommand, input=arg, path=path)
                embed = discord.Embed(
                    title="**Admin Config**", colour=get_embedcolour(ctx.message)
                )
                embed.set_footer(
                    text=FOOTER[0]
                    + str(user)
                    + FOOTER[1]
                    + str(get_author())
                    + FOOTER[2]
                    + str(get_prefix_string(ctx.message)),
                    icon_url=ICON_URL,
                )
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
                embed.set_footer(
                    text=FOOTER[0]
                    + str(user)
                    + FOOTER[1]
                    + str(get_author())
                    + FOOTER[2]
                    + str(get_prefix_string(ctx.message)),
                    icon_url=ICON_URL,
                )
                embed.add_field(
                    name="‎",
                    value="Das Modul **" + str(subcommand) + "** existiert nicht!",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()

    @adminconfig.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                title="**Fehler**", colour=get_embedcolour(ctx.message)
            )
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "config <Guild ID> <Modul> <Wert>```",
                inline=False,
            )
            await ctx.send(embed=embed)


########################################################################################################################


def setup(bot):
    bot.add_cog(adminconfig(bot))
