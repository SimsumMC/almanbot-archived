import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR


class unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unmute", aliases=["um"], usage="<@Nutzer>")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Muted")
        if botchannel_check(ctx):
            try:
                await member.remove_roles(mutedrole)
                embed = discord.Embed(
                    title="**Unmute**", colour=get_embedcolour(ctx.message)
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
                embed.add_field(name="Moderator", value=str(mention), inline=False)
                embed.add_field(name="Nutzer", value=str(member.mention), inline=False)
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + f": Der Moderator {user} hat den Nutzer {member} unmuted.",
                    guildid=ctx.guild.id,
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
                    text=str(time)
                    + ": Der Bot hatte nicht die nötigen Berrechtigungen um "
                    + get_prefix_string(ctx.message)
                    + "unmute auszuführen..",
                    guildid=ctx.guild.id,
                )
        else:
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "unmute im Channel #"
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

    @unmute.error
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
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hatte nicht die nötigen Berrechtigungen um "
                + get_prefix_string(ctx.message)
                + "unmute zu nutzen.",
                guildid=ctx.guild.id,
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
                + "unmute <@Nutzer>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "unmute eingegeben.",
                guildid=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(unmute(bot))
