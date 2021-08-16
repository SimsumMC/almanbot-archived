import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
    get_blacklist,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.func_json import writejson
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR


class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def blacklist(self, ctx, type, *, word):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        path = os.path.join("data", "blacklist", f"{ctx.guild.id}.json")
        bannedWords = get_blacklist(path)
        if botchannel_check(ctx):
            if type == "add":
                if word.lower() in bannedWords:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=f"Das Wort ```{word}```"
                        " ist bereits auf der Blacklist!",
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
                    log(
                        f'{time}: Der Moderator {user} hat versucht das Wort "{word}" zur Blacklist hinzufügen,'
                        " es war aber schon drauf.",
                        id=ctx.guild.id,
                    )
                else:
                    bannedWords.append(word.lower())
                    writejson(type="blacklist", input=bannedWords, path=path)
                    await msg2.delete()
                    embed = discord.Embed(
                        title="**Blacklist**",
                        description=f"Das Wort ```{word}```"
                        " wurde zur Blacklist hinzugefügt!",
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
                    log(
                        f'{time}: Der Moderator {user} hat das Wort "{word}" auf die Blacklist hinzugefügt.',
                        id=ctx.guild.id,
                    )
            elif type == "remove":
                if word.lower() in bannedWords:
                    bannedWords.remove(word.lower())
                    writejson(type="blacklist", input=bannedWords, path=path)
                    await ctx.message.delete()
                    embed = discord.Embed(
                        title="**Blacklist**",
                        description=f"Das Wort ```{word}```"
                        " wurde von der Blacklist entfernt!",
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
                    log(
                        f'{time}: Der Moderator {user} hat das Wort "{word}"von der Blacklist entfernt.',
                        id=ctx.guild.id,
                    )
                else:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=f"Das Wort ```{word}```"
                        " befindet sich nicht auf der Blacklist!",
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
                    log(
                        f'{time}: Der Moderator {user} hat versucht das Wort "{word}" von der Blacklist zu entfernen,'
                        " es war aber nicht drauf.",
                        id=ctx.guild.id,
                    )
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
                    value="Du hast ein ungültiges Argument angegeben, Nutzung: ```"
                    + get_prefix_string(ctx.message)
                    + "blacklist <add/new>```",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Moderator {user} hat ein ungültiges Argument beim Befehl"
                    + get_prefix_string(ctx.message)
                    + "blacklist eingegeben.",
                    ctx.guild.id,
                )
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "blacklist im Channel #"
                + str(name)
                + " zu benutzen!",
                id=ctx.guild.id,
            )
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

    @blacklist.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
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
                value="Dir fehlt folgende Berrechtigung um den Befehl auszuführen: "
                "```ban_members```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um "
                + get_prefix_string(ctx.message)
                + "blacklist zu nutzen.",
                id=ctx.guild.id,
            )
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
                + "blacklist <new/add> <Wort>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "blacklist eingegeben.",
                id=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(blacklist(bot))
