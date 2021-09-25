import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_levelling import get_rank_card
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.logging import log


class rank(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="rank")
    @commands.cooldown(1, 5, BucketType.guild)
    async def rank(self, ctx, member: discord.Member = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        if not member:
            member = ctx.author
        if member.bot:  # TODO : Error
            return
        file = discord.File(fp=await get_rank_card(member=member, guild=ctx.guild), filename="rank.png")
        await ctx.send(file=file)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "rank benutzt!",
            guildid=ctx.guild.id,
        )


def setup(bot):
    bot.add_cog(rank(bot))
