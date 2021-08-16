import datetime
import discord
import whois
from discord.ext import commands

from cogs.core.config.config_botchannel import get_botchannel_obj_list, botchannel_check
from cogs.core.functions.functions import get_author, get_botc, whoisr
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log
from config import FOOTER, ICON_URL, THUMBNAIL_URL, WRONG_CHANNEL_ERROR


class example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def example(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            embed = discord.Embed(title='', colour=get_embedcolour(ctx.message))
            embed.set_thumbnail(
                url=THUMBNAIL_URL)
            embed.add_field(name='‎', value='', inline=False)
            embed.set_footer(
                text=FOOTER[0]
                     + str(user)
                     + FOOTER[1]
                     + str(get_author())
                     + FOOTER[2]
                     + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            await ctx.send(embed=embed)
            log(f'{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}'
                'meme benutzt!', id=ctx.guild.id)
        else:
            log(input=f'{time}: Der Nutzer {user} hat probiert den Befehl {get_prefix_string(ctx.message)}'
                      f'example im Channel #{name} zu benutzen!', id=ctx.guild.id)
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
    bot.add_cog(example(bot))
