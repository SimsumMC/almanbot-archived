import datetime
import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR


class serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            embed = discord.Embed(
                title=f"**Serverinfo für {ctx.guild.name}**",
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
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="**Name:**", value=ctx.guild.name, inline=True)
            embed.add_field(name="**ID:**", value=ctx.guild.id, inline=True)
            embed.add_field(name="**Region:**", value=ctx.guild.region, inline=True)
            embed.add_field(
                name="**Erstellt am:**",
                value=ctx.guild.created_at.strftime("%d.%m.%y um %H:%M"),
                inline=True,
            )
            embed.add_field(
                name="**Besitzer:**", value=ctx.guild.owner.mention, inline=True
            )
            embed.add_field(
                name="**Spielerzahlen:**",
                value=f"Gesamt: `{ctx.guild.member_count}`\n"
                "Spieler: "
                f"`{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}`\n"
                "Bots: "
                f"`{len(list(filter(lambda m: m.bot, ctx.guild.members)))}`\n",
                inline=True,
            )
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl  "
                + get_prefix_string(ctx.message)
                + "serverinfo benutzt!",
                ctx.guild.id,
            )
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "serverinfo im Channel #"
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


########################################################################################################################


def setup(bot):
    bot.add_cog(serverinfo(bot))
