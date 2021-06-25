import datetime
import os
import qrcode
import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour, get_botname


def make_qr(filename, msg):
    img = qrcode.make(msg)
    img.save(filename)


class qr(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qr(self, ctx, *, link):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        path = f'qrcode by {get_botname()}.png'
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            make_qr(str(path), link)
            embed = discord.Embed(title="**QR Code**", colour=get_colour(ctx.message))
            file = discord.File(path, filename="image.png")
            embed.set_image(url="attachment://image.png")
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                    '.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            await ctx.send(file=file, embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat mit dem Befehl !qr einen QRCODE des Links ' + str(
                link) + ' generiert!', ctx.guild.id)
            os.remove(path)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'qr im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @qr.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'qr <Link>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'qr eingegeben.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(qr(bot))
