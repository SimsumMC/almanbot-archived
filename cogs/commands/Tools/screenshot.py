import datetime
import os
import traceback

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from discord_components import Button, ButtonStyle
from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log
from config import ABSTRACT_API_KEY


class screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="screenshot", aliases=["bildschirmfoto", "screen"], usage="<Websitelink>"
    )
    @commands.cooldown(1, 5, BucketType.guild)
    async def screenshot(self, ctx: commands.Context, url):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        if not url.startswith("http"):
            embed = discord.Embed(
                title="**Fehler**",
                description="Du musst eine gültige URL angeben!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}screenshot einen Screenshot zu erstellen, hat dabei aber einen ungültigen Link angegeben!",
                guildid=ctx.guild.id,
            )
            return
        try:
            filename = f"screen-{ctx.author.id}.png"
            async with ctx.typing():
                url = f"https://screenshot.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&url={url}&capture_full_page=false&delay=3&export_format=png"
                async with aiohttp.ClientSession() as session:
                    async with session.request("GET", url) as response:
                        img = await response.read()
                        with open(filename, "wb") as f:
                            f.write(img)
            file = discord.File(filename, filename="screen.png")
            embed = discord.Embed(
                title="**Screenshot**", colour=await get_embedcolour(ctx.message)
            )
            embed.set_image(url=f"attachment://screen.png")
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(
                file=file,
                embed=embed,
                components=[
                    Button(style=ButtonStyle.URL, url=url, label="Zur Website")
                ],
            )
            os.remove(filename)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {await get_prefix_string(ctx.message)}"
                f"screenshot einen Screenshot der Seite {url} erstellt!",
                guildid=ctx.guild.id,
            )
        except Exception:
            embed = discord.Embed(
                title="**Fehler**",
                description="Es konnte kein Screenshot erstellt werden!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}screenshot einen Screenshot der Website {url} zu erstellen, dabei trat ein Fehler auf!",
                guildid=ctx.guild.id,
            )
            traceback.print_exc()


########################################################################################################################


def setup(bot):
    bot.add_cog(screenshot(bot))
