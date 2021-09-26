import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_levelling import get_rank_card
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
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
        if member.bot:
            embed = discord.Embed(
                title="**Fehler**",
                description="Bots sind vom Levelsystem ausgeschlossen und verdienen daher keine XP!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}rank das Level eines Bots einzusehen!",
                guildid=ctx.guild.id,
            )
            return
        file = discord.File(
            fp=await get_rank_card(member=member, guild=ctx.guild), filename="rank.png"
        )
        await ctx.send(file=file)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "rank benutzt!",
            guildid=ctx.guild.id,
        )


def setup(bot):
    bot.add_cog(rank(bot))
