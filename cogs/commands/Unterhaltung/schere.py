import datetime
import random

import discord
from discord.ext import commands

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class schere(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schere(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            schere = ['Ich hatte auch die Schere, Unentschieden!',
                      'Du hast gewonnen, ich hatte mich für das Papier entschieden!',
                      'Guter Versuch, aber ich habe aber mit dem Stein gewonnen!']
            schererandom = random.choice(schere)
            embed = discord.Embed(title='**Schere Stein Papier**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎', value=str(schererandom), inline=False)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'schere benutzt!', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'schere im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(schere(bot))