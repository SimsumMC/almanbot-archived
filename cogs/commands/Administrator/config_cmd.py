import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument

from config import ICON_URL, THUMBNAIL_URL, FOOTER
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
    writejson,
    readjson,
)
from cogs.core.config.config_memes import get_memes, redditnsfwcheck, meme_is_checked
from cogs.core.config.config_colours import get_colour, get_colour_code, colour_check
from cogs.core.functions.logging import log


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, subcommand, arg="hilfe"):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        channel = get_botc(message=ctx.message)
        existing = [
            "prefix",
            "botchannel",
            "memechannel",
            "memesource",
            "colour",
            "hilfe",
        ]
        if True:  # removed Channel Check
            if subcommand in existing:
                if subcommand == "colour":
                    if colour_check(arg) is True:
                        writejson(
                            type=subcommand, input=get_colour_code(str(arg)), path=path
                        )
                        embed = discord.Embed(
                            title="**Config**",
                            description="Das Modul ```"
                            + str(subcommand)
                            + "``` wurde erfolgreich zu ```"
                            + str(arg)
                            + "``` geändert!",
                            colour=get_colour(ctx.message),
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
                        log(
                            input=str(time)
                            + ": Der Spieler "
                            + str(user)
                            + " hat den Befehl "
                            + get_prefix_string(ctx.message)
                            + "config benutzt und damit das "
                            "Modul "
                            + str(subcommand)
                            + " zu "
                            + str(arg)
                            + " erfolgreich geändert",
                            id=ctx.guild.id,
                        )
                        return
                    else:
                        embed = discord.Embed(
                            title="**Fehler**",
                            description="Das Modul ```"
                            + str(subcommand)
                            + "``` kann nicht zu ```"
                            + str(arg)
                            + "``` geändert werden.",
                            colour=get_colour(ctx.message),
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
                        log(
                            input=str(time)
                            + ": Der Spieler "
                            + str(user)
                            + " hat probiert das Modul "
                            + str(subcommand)
                            + " zu "
                            + str(arg)
                            + " zu ändern.",
                            id=ctx.guild.id,
                        )
                        return
                elif subcommand == "hilfe":
                    embed = discord.Embed(
                        title="**Config Hilfe**",
                        description="Hier findest du alle Subbefehle zum !config Befehl!",
                        colour=get_colour(ctx.message),
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
                    embed.add_field(
                        name=f"**{get_prefix_string(ctx.message)}config prefix <Präfix>**",
                        value="Ändere den Prefix deines Bots, der in der Konsole angezeigt wird!",
                        inline=False,
                    )
                    embed.add_field(
                        name=f'**{get_prefix_string(ctx.message)}config colour <Farbe / "random">**',
                        value="Ändere die Farbe der Embeds.",
                        inline=False,
                    )
                    embed.add_field(
                        name=f'**{get_prefix_string(ctx.message)}config botchannel <name / "None">**',
                        value="Sorge dafür das die Befehle nur in einem bestimmten Kanal funktionieren!",
                        inline=False,
                    )
                    embed.add_field(
                        name=f'**{get_prefix_string(ctx.message)}config memechannel <name / "None">**',
                        value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
                        inline=False,
                    )
                    embed.add_field(
                        name=f'**{get_prefix_string(ctx.message)}config memesource <Reddit Name / "default"'
                        ">**",
                        value="Sorge dafür das der Meme Befehl nur in einem bestimmten Kanal funktioniert!",
                        inline=False,
                    )
                    await ctx.send(embed=embed)
                    log(
                        input=str(time)
                        + ": Der Spieler "
                        + str(user)
                        + " hat den Befehl "
                        + get_prefix_string(ctx.message)
                        + "config hilfe benutzt.",
                        id=ctx.guild.id,
                    )
                    return
                if subcommand == "memesource":
                    path2 = os.path.join("data", "verifiedmemes", "memes.json")
                    if arg == "default":
                        arg = "memes"
                    if (
                        arg != get_memes(ctx.guild.id)
                        and meme_is_checked(arg) is False
                    ):
                        if arg in readjson("failed", path2) or redditnsfwcheck(arg):
                            embed = discord.Embed(
                                title="**Fehler**",
                                description=f"Der angegebene Reddit **{arg}** enthält nicht "
                                "zulässigen Inhalt.",
                                color=get_colour(ctx.message),
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
                            log(
                                input=str(time)
                                + ": Der Spieler "
                                + str(user)
                                + " hat probiert den Befehl "
                                + get_prefix_string(ctx.message)
                                + "config zu benutzen und damit das "
                                "Modul "
                                + str(subcommand)
                                + " zu"
                                + str(arg)
                                + " zu ändern.",
                                id=ctx.guild.id,
                            )
                            return
                writejson(type=subcommand, input=arg, path=path)
                embed = discord.Embed(
                    title="**Config**", colour=get_colour(ctx.message)
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
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + " hat den Befehl "
                    + get_prefix_string(ctx.message)
                    + "config benutzt und damit das "
                    "Modul "
                    + str(subcommand)
                    + " zu"
                    + str(arg)
                    + " erfolgreich geändert",
                    id=ctx.guild.id,
                )
            else:
                embed = discord.Embed(
                    title="**Fehler**", colour=get_colour(ctx.message)
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
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + " hat probiert den Befehl "
                    + get_prefix_string(ctx.message)
                    + "config zu benutzen und damit das "
                    "Modul " + str(subcommand) + " zu" + str(arg) + " zu ändern.",
                    id=ctx.guild.id,
                )
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "serverlog im Channel #"
                + str(channel)
                + " zu benutzen!",
                id=ctx.guild.id,
            )
            await ctx.send(
                str(mention)
                + ", dieser Befehl kann nur im Kanal #{} genutzt werden.".format(
                    channel
                ),
                delete_after=3,
            )
            await msg2.delete()

    @config.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="**Fehler**", colour=get_colour(ctx.message))
            embed.set_footer(
                text="for "
                + str(user)
                + " | by "
                + str(get_author())
                + " | Prefix "
                + get_prefix_string(message=ctx.message),
                icon_url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739"
                "/winging-easy.png?width=676&height=676",
            )
            embed.add_field(
                name="‎",
                value="Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um "
                + get_prefix_string(ctx.message)
                + "config zu nutzen.",
                id=ctx.guild.id,
            )
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title="**Fehler**", colour=get_colour(ctx.message))
            embed.set_footer(
                text="for "
                + str(user)
                + " | by "
                + str(get_author())
                + " | Prefix "
                + get_prefix_string(message=ctx.message),
                icon_url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739"
                "/winging-easy.png?width=676&height=676",
            )
            embed.add_field(
                name="‎",
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "config <Modul/hilfe> <Wert>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "config eingegeben.",
                id=ctx.guild.id,
            )
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="**Cooldown**",
                description=f"Versuch es nochmal in {error.retry_after:.2f}s.",
                color=get_colour(ctx.message),
            )
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy"
                ".png?width=676&height=676"
            )
            embed.set_footer(
                text="for "
                + str(user)
                + " | by "
                + str(get_author())
                + " | Prefix "
                + str(get_prefix_string(message=ctx.message)),
                icon_url="https://media.discordapp.net/attachments/645276319311200286"
                "/803322491480178739/winging-easy.png?width=676&height=676",
            )
            await ctx.send(embed=embed)
            log(
                f"{time}: Der Spieler {user} hat trotz eines Cooldowns versucht den Befehl'"
                f"'{get_prefix_string(ctx.message)}config im Kanal #{ctx.channel.name} zu nutzen.",
                ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(config(bot))
