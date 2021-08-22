import datetime
import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from cogs.core.functions.functions import (
    get_author,
    whoisr,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR


class nutzerinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["userinfo", "whois", "userstats", "nutzerstats"])
    async def nutzerinfo(self, ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            if member is None:
                member = ctx.author
            roles = [role for role in member.roles]
            embed = discord.Embed(
                title=f"**Nutzerinfo für {member.display_name}**",
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
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name="**Nutzername:**", value=member.display_name, inline=True
            )
            embed.add_field(name="**ID:**", value=member.id, inline=True)

            embed.add_field(name="**Tag:**", value=member.discriminator, inline=True)
            embed.add_field(
                name="Aktuelle Aktivität:",
                value=f" {member.activity.name}"
                if member.activity is not None
                else "Keine",
                inline=True,
            )
            embed.add_field(
                name="**Erstellt am:**",
                value=member.created_at.strftime("%d.%m.%y um %H:%M"),
                inline=True,
            )
            embed.add_field(
                name="**Beigetreten am:**",
                value=member.joined_at.strftime("%d.%m.%y um %H:%M"),
                inline=True,
            )
            embed.add_field(
                name=f"**Rollen ({len(roles) - 1}):**",
                value="".join([role.mention for role in roles]),
                inline=True,
            )
            embed.add_field(
                name="**Höchste Rolle:**", value=member.top_role.mention, inline=True
            )
            embed.add_field(
                name="**Bot?:**", value=str(whoisr(member=member)), inline=True
            )
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl  "
                + get_prefix_string(ctx.message)
                + "nutzerinfo benutzt!",
                ctx.guild.id,
            )
            print("final")
        else:
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "nutzerinfo im Channel #"
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


########################################################################################################################


def setup(bot):
    bot.add_cog(nutzerinfo(bot))
