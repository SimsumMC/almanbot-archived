import datetime
import random
import discord
from discord.ext import commands
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class münzwurf(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["münze", "coin", "coinflip"])
    async def münzwurf(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            embed = discord.Embed(title='**Münzwurf**', colour=get_colour(ctx.message))
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/851853486948745246/851853555731529768/"
                                    "munzwurf.png")
            embed.add_field(name='‎', value='', inline=False)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(f'{time}: Der Spieler {user} hat den Befehl {get_prefix_string(ctx.message)}'
                'münzwurf benutzt!', id=ctx.guild.id)
        else:
            log(input=f'{time}: Der Spieler {user} hat probiert den Befehl {get_prefix_string(ctx.message)}'
                      f'münzwurf im Channel #{name} zu benutzen!', id=ctx.guild.id)
            await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
                           delete_after=3)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(münzwurf(bot))