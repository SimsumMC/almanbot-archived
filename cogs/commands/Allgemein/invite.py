import datetime
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import (
    ICON_URL,
    THUMBNAIL_URL,
    FOOTER,
    WRONG_CHANNEL_ERROR,
    INVITE_LINK,
    DISCORD_LINK,
    WEBSITE_LINK,
)


class invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Invite**", color=get_embedcolour(ctx.message)
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
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.add_field(
                name="**Link**",
                value=INVITE_LINK,
            )
            await ctx.send(
                embed=embed,
                components=[
                    [
                        Button(
                            style=ButtonStyle.URL,
                            label="Klicke hier um mich zu einem Server hinzuzufügen!",
                            url=INVITE_LINK,
                        ),
                        Button(
                            style=ButtonStyle.URL,
                            label="Discord",
                            url=DISCORD_LINK,
                        ),
                        Button(
                            style=ButtonStyle.URL,
                            label="Website",
                            url=WEBSITE_LINK,
                        ),
                    ]
                ],
            )

            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl  "
                + get_prefix_string(ctx.message)
                + "invite benutzt!",
                ctx.guild.id,
            )
        else:
            log(
                text=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "invite im Channel #"
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
    bot.add_cog(invite(bot))
