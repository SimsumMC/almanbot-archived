import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, ButtonStyle

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from config import (
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
        if await botchannel_check(ctx):
            embed = discord.Embed(
                title="**Invite**", color=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
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

            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl  "
                + await get_prefix_string(ctx.message)
                + "invite benutzt!",
                ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(invite(bot))
