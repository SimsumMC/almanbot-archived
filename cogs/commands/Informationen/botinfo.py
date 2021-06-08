import datetime
import discord
from discord.ext import commands
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour
from main import client


class botinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def botinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            ergebnis = 0
            for guild in client.guilds:
                ergebnis += guild.member_count
            embed = discord.Embed(title='**Botinfo**', color=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='**Entwickler**', value='SimsumMC#3579', inline=True)
            embed.add_field(name='**Projektbeginn**', value='Anfang 2021', inline=True)
            embed.add_field(name='**Arbeitszeit**', value='ca. 40 Stunden', inline=True)
            embed.add_field(name='**Server**', value=f'{len(client.guilds)}', inline=True)
            embed.add_field(name='**Nutzer**', value=f'{ergebnis}', inline=True)
            embed.add_field(name='**Source**', value='[Github](https://github.com/SimsumMC/communitybot)', inline=True)
            embed.add_field(name='**Website**', value='[Link](https://communitybot.visitlink.de/)', inline=True)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl  ' +
                get_prefix_string(ctx.message) + 'botinfo benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'botinfo im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

########################################################################################################################


def setup(bot):
    bot.add_cog(botinfo(bot))