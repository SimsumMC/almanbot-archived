import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="levelling", aliases=["levelsettings"])
    @commands.has_permissions(administrator=True)
    async def levelling(self, ctx: commands.Context):
        await ctx.invoke(self.levelling_help)

    @levelling.command(name="help", aliases=["hilfe"])
    @commands.has_permissions(administrator=True)
    async def levelling_help(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="Levelling Help",
            description=f"Hier findest du alle Sub-Befehle zum Befehl `{prefix}levelling` !",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name=f"**{prefix}levelling roles**",
            value="Zeigt dir alle Levelling-Rollen an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling settings**",
            value="Zeigt dir alle Settings des Levelsystems an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling disable / enable**",
            value="Aktiviere / Deaktiviere das Levelsystem!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling set <Einstellung> <Wert>**",
            value="Weise einer Einstellungsmöglichkeit einen bestimmten Wert zu!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            "levelling hilfe benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(levelling(bot))
