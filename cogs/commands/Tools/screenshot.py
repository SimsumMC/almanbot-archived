import datetime
import os
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, ButtonStyle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log
from config import CHROMEDRIVER_PATH


class screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="screenshot", aliases=["bildschirmfoto", "screen"], usage="<Websitelink>"
    )
    @commands.is_nsfw()
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
            async with ctx.typing():  # takes a bit of time
                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Chrome(
                    executable_path=CHROMEDRIVER_PATH, chrome_options=options
                )
                driver.set_window_size(1225, 800)
                driver.get(url)
                driver.save_screenshot("screen.png")
                file = discord.File("screen.png", filename="screen.png")
            embed = discord.Embed(
                title="**Screenshot**", colour=await get_embedcolour(ctx.message)
            )
            embed.set_image(url="attachment://screen.png")
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(
                file=file,
                embed=embed,
                components=[
                    Button(style=ButtonStyle.URL, url=url, label="Zur Website")
                ],
            )

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
        os.remove("screen.png")


########################################################################################################################


def setup(bot):
    bot.add_cog(screenshot(bot))
