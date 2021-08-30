import datetime
import os
import qrcode
import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, Bot

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import (
    get_author,
    get_botname,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR


def make_qr(filename, msg):
    img = qrcode.make(msg)
    img.save(filename)


class qr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qr", usage="<Text>")
    async def qr(self, ctx, *, text):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        path = f"qrcode by {get_botname()}.png"
        if botchannel_check(ctx):
            make_qr(str(path), text)
            embed = discord.Embed(
                title="**QR Code**", colour=get_embedcolour(ctx.message)
            )
            file = discord.File(path, filename="image.png")
            embed.set_image(url="attachment://image.png")
            embed.set_footer(
                text=FOOTER[0]
                + str(user)
                + FOOTER[1]
                + str(get_author())
                + FOOTER[2]
                + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            await ctx.send(file=file, embed=embed)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat mit dem Befehl !qr einen QRCODE des Links "
                + str(text)
                + " generiert!",
                ctx.guild.id,
            )
            os.remove(path)
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(qr(bot))
