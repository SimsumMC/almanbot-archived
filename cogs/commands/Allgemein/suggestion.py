import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log
from config import SUGGESTION_CHANNEL_ID


class suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="vorschlag", aliases=["suggest", "suggestion"], usage="<Vorschlag>"
    )
    async def vorschlag(self, ctx: commands.Context, *, _suggestion):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        channel = self.bot.get_channel(SUGGESTION_CHANNEL_ID)
        _suggestion = str(_suggestion)
        # Channel Embed
        embed = discord.Embed(
            title="Vorschlag",
            description=_suggestion,
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx, replace=[["für", "von"]])
        embed._thumbnail = await get_embed_thumbnail()
        msg: discord.Message = await channel.send(embed=embed)
        await msg.add_reaction(emoji="✅")
        await msg.add_reaction(emoji="❌")
        # User Embed
        embed = discord.Embed(
            title="Vorschlag", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(
            name="‎",
            value=f"Dein Vorschlag wurde erfolgreich in {channel.mention} gesendet!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "vorschlag benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(suggestion(bot))
