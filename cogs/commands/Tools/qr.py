import datetime
import os

import discord
import qrcode
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.functions import (
    get_botname,
)
from cogs.core.functions.logging import log


async def make_qr(filename, msg):
    qrcode.make(msg).save(filename)


class qr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qr", usage="<Text>")
    async def qr(self, ctx, *, text):
        time = datetime.datetime.now()
        user = ctx.author.name
        path = f"qrcode by {await get_botname()}.png"
        if await botchannel_check(ctx):
            await make_qr(str(path), text)
            embed = discord.Embed(
                title="**QR Code**", colour=await get_embedcolour(ctx.message)
            )
            file = discord.File(path, filename="image.png")
            embed.set_image(url="attachment://image.png")
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(file=file, embed=embed)
            await log(
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
