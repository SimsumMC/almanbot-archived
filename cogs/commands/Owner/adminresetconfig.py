import datetime
import os

import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
)
from cogs.core.config.config_colours import get_colour
from cogs.core.config.config_general import resetconfig


class adminresetconfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def adminresetconfig(self, ctx, guildid):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join("data", "configs", f"{guildid}.json")
        channel = get_botc(message=ctx.message)
        if name == channel or channel == "None":
            if resetconfig(path):
                embed = discord.Embed(
                    title="**Reset Config**",
                    description=f"Die Config vom Server mit der ID```{guildid}```"
                    "wurde erfolgreich zurückgesetzt.",
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
                return
            else:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=f"Die Config vom Server mit der ID```{guildid}```"
                    "konnte nicht zurückgesetzt werden.",
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
                return
        else:
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


########################################################################################################################


def setup(bot):
    bot.add_cog(adminresetconfig(bot))
