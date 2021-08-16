import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            if "#" not in member:
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
                    value="Du musst den Spieler mit dem Tag angeben, also z.B. Spieler#1234 !",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + get_prefix_string(ctx.message)
                    + "unban angegeben.",
                    id=ctx.guild.id,
                )
                return
            elif "<@" in member and ">" in member:
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
                    value="Du musst den Spieler mit dem Tag angeben, also z.B. Spieler#1234 !",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + get_prefix_string(ctx.message)
                    + "unban angegeben.",
                    id=ctx.guild.id,
                )
                return
            try:
                banned_users = await ctx.guild.bans()
                member_name, member_disc = member.split("#")
                for ban_entry in banned_users:
                    user2 = ban_entry.user
                    if (user2.name, user2.discriminator) == (member_name, member_disc):
                        try:
                            await ctx.guild.unban(user2)
                            embed = discord.Embed(
                                title="**Unban**", colour=get_embedcolour(ctx.message)
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
                                name="Moderator:", value=mention, inline=False
                            )
                            embed.add_field(
                                name="Nutzer:", value=str(member), inline=False
                            )
                            await ctx.send(embed=embed)
                            log(
                                str(time)
                                + ": Der Moderator "
                                + str(user)
                                + "hat den Nutzer "
                                + str(member)
                                + " erfolgreich entbannt.",
                                id=ctx.guild.id,
                            )
                        except Exception:
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
                                value="Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!",
                                inline=False,
                            )
                            await ctx.send(embed=embed)
                            log(
                                input=str(time)
                                + ": Der Bot hatte nicht die nötigen Berrechtigungen um "
                                + get_prefix_string(ctx.message)
                                + "unban auszuführen..",
                                id=ctx.guild.id,
                            )
                else:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description="Der Nutzer "
                        + str(member)
                        + " ist nicht gebannt und kann daher "
                        "auch nicht entbannt werden.",
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
                        str(time)
                        + ": Der Moderator "
                        + str(user)
                        + "hat versucht den  ungültigen Nutzer "
                        + str(member)
                        + " zu entbannen.",
                        id=ctx.guild.id,
                    )
            except Exception:
                raise Exception
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "unban im Channel #"
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

    @unban.error
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
                + "unban zu nutzen.",
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
                + "unban <Spieler#1234>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "unban eingegeben.",
                id=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(unban(bot))
