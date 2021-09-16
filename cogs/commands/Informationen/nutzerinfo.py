import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.functions import (
    whoisr,
)
from cogs.core.functions.logging import log


class nutzerinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["userinfo", "userstats", "nutzerstats"])
    async def nutzerinfo(self, ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            if member is None:
                member = ctx.author
            roles = [role for role in member.roles]
            embed = discord.Embed(
                title=f"**Nutzerinfo für {member.display_name}**",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(
                name="**Nutzername:**", value=member.display_name, inline=False
            )
            embed.add_field(name="**ID:**", value=member.id, inline=False)

            embed.add_field(name="**Tag:**", value=member.discriminator, inline=False)
            embed.add_field(
                name="Aktuelle Aktivität:",
                value=f" {member.activity.name}"
                if member.activity is not None
                else "Keine",
                inline=False,
            )
            embed.add_field(
                name="**Erstellt am:**",
                value=member.created_at.strftime("%d.%m.%y um %H:%M"),
                inline=False,
            )
            embed.add_field(
                name="**Beigetreten am:**",
                value=member.joined_at.strftime("%d.%m.%y um %H:%M"),
                inline=False,
            )
            embed.add_field(
                name="**Bot?:**", value=str(await whoisr(member=member)), inline=True
            )
            embed.add_field(
                name=f"**Rollen ({len(roles) - 1}):**",
                value="".join(
                    [
                        role.mention + "\n"
                        for role in roles
                        if not role.name == "@everyone"
                    ]
                )
                if len(roles) != 1
                else "Keine",
                inline=False,
            )
            embed.add_field(
                name="**Höchste Rolle:**",
                value=member.top_role.mention
                if not member.top_role.name == "@everyone"
                else "Keine",
                inline=False,
            )
            await ctx.send(embed=embed)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl  "
                + await get_prefix_string(ctx.message)
                + "nutzerinfo benutzt!",
                ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(nutzerinfo(bot))
