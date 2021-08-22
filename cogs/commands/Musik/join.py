import datetime
import discord
from discord.ext import commands

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.functions.functions import get_author
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import FOOTER, ICON_URL, WRONG_CHANNEL_ERROR


class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        channel = ctx.author.voice.channel
        if botchannel_check(ctx):
            if ctx.author.voice:
                # here connect to vc
                embed = discord.Embed(
                    title="Musik Join", colour=get_embedcolour(ctx.message)
                )
                embed.set_thumbnail(
                    url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png"
                    "?width=676&height=676"
                )
                embed.add_field(name="‎", value="", inline=False)
                embed.set_footer(
                    text="for "
                    + str(user)
                    + " | by "
                    + str(get_author())
                    + " | Prefix "
                    + get_prefix_string(message=ctx.message),
                    icon_url="https://media.discordapp.net/attachments/645276319311200286"
                    "/803322491480178739/winging-easy.png?width=676&height=676",
                )
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Spieler {user} hat den Befehl {get_prefix_string(ctx.message)}"
                    "meme benutzt!",
                    guildid=ctx.guild.id,
                )
            else:
                ...
                # author is in NO voice channel
        else:
            log(
                text=f"{time}: Der Spieler {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                f"example im Channel #{name} zu benutzen!",
                guildid=ctx.guild.id,
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
    bot.add_cog(join(bot))
