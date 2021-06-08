import datetime
import os

import discord
from discord.ext import commands

from cogs.core.functions.functions import get_author, get_prefix_string, get_botc, get_colour, resetconfig


class adminresetconfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def adminresetconfig(self, ctx, guildid):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join('data', 'configs', f'{guildid}.json')
        channel = get_botc(message=ctx.message)
        if name == channel or channel == "None":
            if resetconfig(path):
                embed = discord.Embed(title='**Reset Config**',
                                      description=f'Die Config vom Server mit der ID```{guildid}```'
                                                  'wurde erfolgreich zurückgesetzt.'
                                      , colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed)
                return
            else:
                embed = discord.Embed(title='**Fehler**',
                                      description=f'Die Config vom Server mit der ID```{guildid}```'
                                                  'konnte nicht zurückgesetzt werden.'
                                      , colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed)
                return
        else:
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()


########################################################################################################################


def setup(bot):
    bot.add_cog(adminresetconfig(bot))
