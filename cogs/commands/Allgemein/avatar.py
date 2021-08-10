import datetime

import discord
from discord.ext import commands
from discord.ext.commands import BadArgument

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
)
from cogs.core.config.config_colours import get_colour
from cogs.core.functions.logging import log


class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            if member is None:
                member = ctx.author
            embed = discord.Embed(
                title=f"**Avatar von {member.display_name}**",
                colour=get_colour(ctx.message),
            )
            embed.set_image(url=member.avatar_url)
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
                f"{time}: Der Spieler {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "avatar benutzt!",
                id=ctx.guild.id,
            )
        else:
            log(
                input=f"{time}: Der Spieler {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                f"avatar im Channel #{name} zu benutzen!",
                id=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**", description=WRONG_CHANNEL_ERROR, colour=get_colour(message=ctx.message)
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

    @avatar.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, BadArgument):
            embed = discord.Embed(title="**Fehler**", colour=get_colour(ctx.message))
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
                value="Du musst den Spieler erwähnen, also z.B. @Spieler#1234 !",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat ein ungültiges Argument bei "
                + get_prefix_string(ctx.message)
                + "avatar angegeben.",
                id=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(avatar(bot))
