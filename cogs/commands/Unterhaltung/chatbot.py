import datetime
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chatbot", aliases=["ai", "ki", "chat"], usage="<Nachricht>")
    async def chatbot(self, ctx: commands.Context, *, message):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        url = f"https://api.pgamerx.com/v5/ai"
        headers = {
            "Authorization": "EWuDPCUXqCKo",
        }
        params = {"message": message, "server": "main"}
        async with aiohttp.ClientSession() as session:
            async with session.request(
                "GET", url, headers=headers, params=params
            ) as response:
                if response.status != 200:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description="Ich hab leider vergessen was du gesagt hast, bitte versuch es nochmal!",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._thumbnail = await get_embed_thumbnail()
                    embed._footer = await get_embed_footer(ctx)
                    await ctx.send(embed=embed)
                    await log(
                        text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}chatbot eine Antwort zu bekommen, die API hatte aber einen Fehler!",
                        guildid=ctx.guild.id,
                    )
                    return
                json = await response.json()
                embed = discord.Embed(
                    title="Chatbot",
                    description=str(json[0]["response"]),
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
                    "chatbot benutzt!",
                    guildid=ctx.guild.id,
                )


########################################################################################################################


def setup(bot):
    bot.add_cog(chatbot(bot))
