import datetime
import discord
from discord.ext import commands
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour
from main import client


class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        ping = round(client.latency * 1000)
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            embed = discord.Embed(title='**Ping**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            embed.add_field(name='‎', value=f'Mein  Ping beträgt aktuell {ping}ms!', inline=False)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(user) + f' hat sich den Ping ({str(ping)}ms) ausgeben lassen.'
                , id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'qr im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(ping(bot))