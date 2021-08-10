import datetime
import discord

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, BadArgument
from discord_components import Button, ButtonStyle
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
)
from cogs.core.config.config_colours import get_colour
from cogs.core.functions.logging import log


class loeschdich(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["löschdich", "delteyou", "deletuser", "löschenutzer"])
    async def loeschdich(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            if reason is None:
                reason = "Kein Grund angegeben, den kennst du bestimmt selber!"
            link = f"https://löschdich.de/{member.display_name}"
            link = link.split()[0]
            embed = discord.Embed(
                title=f"**Lösch dich {member.display_name}!**",
                colour=get_colour(ctx.message),
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(name="**Link**", value=f"{link}", inline=False)
            embed.add_field(name="**Grund**", value=str(reason), inline=False)
            await ctx.send(
                content=f"{member.mention}, bitte lösch dich einfach aus dem Internet. Klicke "
                f"dazu einfach unten auf den Knopf für mehr Informationen! ",
                embed=embed,
                components=[
                    Button(
                        style=ButtonStyle.URL,
                        label="Lösch dich Jetzt!",
                        url=link,
                        emoji="🗑",
                    )
                ],
            )
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "löschdich benutzt!",
                id=ctx.guild.id,
            )
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "löschdich im Channel #"
                + str(name)
                + " zu benutzen!",
                id=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**", description=WRONG_CHANNEL_ERROR, colour=get_colour(message=ctx.message)
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

    @loeschdich.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title="**Fehler**", colour=get_colour(ctx.message))
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
                value="Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```"
                + get_prefix_string(ctx.message)
                + "löschdich <@Spieler> <opt. Grund>```",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat nicht alle erforderlichen Argumente beim Befehl "
                + get_prefix_string(ctx.message)
                + "löschdich eingegeben.",
                id=ctx.guild.id,
            )
        if isinstance(error, BadArgument):
            embed = discord.Embed(title="**Fehler**", colour=get_colour(ctx.message))
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
                value="Du musst den Spieler mit dem Tag angeben, also z.B. Spieler#1234 !",
                inline=False,
            )
            await ctx.send(embed=embed)
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat ein ungültiges Argument bei "
                + get_prefix_string(ctx.message)
                + "löschdich angegeben.",
                id=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(loeschdich(bot))
