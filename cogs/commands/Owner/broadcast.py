import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from config import DEFAULT_BROADCAST_MESSAGE


class broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="broadcast", aliases=["ankündigung", "ownermsg", "rundruf"])
    @commands.is_owner()
    async def broadcast(self, ctx, *, message):
        if await botchannel_check(ctx):
            embed = discord.Embed(
                title="**Broadcast**",
                description=DEFAULT_BROADCAST_MESSAGE + "\n\n" + str(message),
                colour=await get_embedcolour(message=ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            aldready_messaged = []
            failed = []
            for guild in self.bot.guilds:
                owner = guild.owner
                if owner.id in aldready_messaged:
                    continue
                try:
                    await owner.send(embed=embed)
                except Exception:
                    failed.append(owner.id)
                aldready_messaged.append(owner.id)
            embed2 = discord.Embed(
                title="**Broadcast**",
                description="Erfolgreich versendet!",
                colour=await get_embedcolour(message=ctx.message),
            )
            if failed:
                embed2.add_field(name="Fehler", value="".join([id for id in failed]))
            embed2._footer = await get_embed_footer(ctx)
            embed2._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed2)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


###############################################################################################################


def setup(bot):
    bot.add_cog(broadcast(bot))
