import datetime
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from cogs.core.functions.functions import log, get_author, get_prefix_string
from main import client


class channelclear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channelclear(self, ctx):
        channelid = ctx.channel.id
        channel1 = client.get_channel(channelid)
        time = datetime.datetime.now()
        user = ctx.author.name
        await channel1.clone()
        await channel1.delete()
        log(input=str(time) + ': Der Spieler ' + str(user) + ' hat den Chat "#' + str(channel1) + '" gecleart.',
            id=ctx.guild.id)

    @channelclear.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title='**Fehler**', colour=13372193)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um ' +
                      get_prefix_string(ctx.message) + 'channelclear zu nutzen.', id=ctx.guild.id)

########################################################################################################################


def setup(bot):
    bot.add_cog(channelclear(bot))