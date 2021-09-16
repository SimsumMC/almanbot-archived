import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.logging import log


class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            if member is None:
                member = ctx.author
            embed = discord.Embed(
                title=f"**Avatar von {member.display_name}**",
                colour=await get_embedcolour(ctx.message),
            )
            embed.set_image(url=member.avatar_url)
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                "avatar benutzt!",
                guildid=ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(avatar(bot))
