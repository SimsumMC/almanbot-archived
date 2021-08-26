import datetime
import discord
import whois
from discord.ext import commands
from cogs.core.functions.functions import get_author, get_botc, whoisr
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class guessthenumber(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guessthenumber(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            embed = discord.Embed(title='', colour=get_embedcolour(ctx.message))
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            embed.add_field(name='‎', value='', inline=False)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(f'{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}'
                'meme benutzt!', guildid=ctx.guild.id)
        else:
            log(text=f'{time}: Der Nutzer {user} hat probiert den Befehl {get_prefix_string(ctx.message)}'
                      f'example im Channel #{name} zu benutzen!', guildid=ctx.guild.id)
            await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
                           delete_after=3)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(guessthenumber(bot))