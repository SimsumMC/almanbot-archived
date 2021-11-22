import datetime
import traceback

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class fox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fox", aliases=["fuchs"])
    async def fox(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        try:
            url = f"https://randomfox.ca/floof/"
            async with aiohttp.ClientSession() as session:
                async with session.request("GET", url) as response:
                    data = await response.json()
            embed = discord.Embed(
                title="Fox", colour=await get_embedcolour(ctx.message)
            )
            embed._footer = await get_embed_footer(ctx)
            embed.set_image(url=data["image"])
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                "fox benutzt!",
                guildid=ctx.guild.id,
            )
        except Exception:
            traceback.print_exc()
            embed = discord.Embed(
                title="**Fehler**",
                description="Es gab einen Fehler bei der API Anfrage. Bitte warte kurz und versuche es erneut!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}fox zu nutzen, es kam aber dabei zu einem API Fehler!",
                guildid=ctx.guild.id,
            )
            return


########################################################################################################################


def setup(bot):
    bot.add_cog(fox(bot))
