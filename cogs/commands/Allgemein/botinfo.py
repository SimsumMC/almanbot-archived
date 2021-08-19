import datetime
import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from main import client
from config import (
    ICON_URL,
    THUMBNAIL_URL,
    FOOTER,
    BOT_MAIN_DEVELOPER,
    BOT_DEVELOPERLIST,
    GITHUB_LINK,
    WEBSITE_LINK,
    WRONG_CHANNEL_ERROR, ABOUT,
)


def get_developer_string():
    if len(BOT_DEVELOPERLIST) == 1:
        return BOT_MAIN_DEVELOPER
    return "".join([dev + " ," for dev in BOT_DEVELOPERLIST])[:-1]


def get_member_count():
    ergebnis = 0
    for guild in client.guilds:
        ergebnis += guild.member_count
    return int(ergebnis)


class botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo", aliases=["info", "about", "bot"])
    async def botinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            embed = discord.Embed(
                title="**Botinfo**", description=ABOUT, color=get_embedcolour(ctx.message)
            )
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )

            embed.add_field(
                name="**Entwickler**", value=get_developer_string(), inline=True
            )
            embed.add_field(name="**Projektbeginn**", value="Anfang 2021", inline=True)
            embed.add_field(name="**Arbeitszeit**", value="ca. 50 Stunden", inline=True)
            embed.add_field(
                name="**Server**", value=f"{len(client.guilds)}", inline=True
            )
            embed.add_field(
                name="**Nutzer**", value=f"{get_member_count()}", inline=True
            )
            embed.add_field(
                name="**Source**",
                value=f"[Github]({GITHUB_LINK})",
                inline=True,
            )
            embed.add_field(
                name="**Website**",
                value=f"[Link]({WEBSITE_LINK})",
                inline=True,
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            await ctx.send(embed=embed)
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl  "
                + get_prefix_string(ctx.message)
                + "botinfo benutzt!",
                ctx.guild.id,
            )
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "botinfo im Channel #"
                + str(name)
                + " zu benutzen!",
                id=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(botinfo(bot))
