import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_general import resetconfig
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail


class adminresetconfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def adminresetconfig(self, ctx, guildid):
        if await botchannel_check(ctx):
            if await resetconfig(guildid):
                embed = discord.Embed(
                    title="**Reset Config**",
                    description=f"Die Config vom Server mit der ID```{guildid}```"
                    "wurde erfolgreich zurückgesetzt.",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=f"Die Config vom Server mit der ID```{guildid}```"
                    "konnte nicht zurückgesetzt werden.",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                return
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(adminresetconfig(bot))
