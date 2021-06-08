import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from cogs.core.functions.functions import get_botc, log, get_author, get_prefix_string, get_colour, redditnsfwcheck


class botlog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def botlog(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join('data', 'logs', f'{ctx.guild.id}.txt')
        channel = get_botc(message=ctx.message)
        if name == channel or channel == "None":
            if os.path.isfile(path):
                await ctx.send(file=discord.File(path))
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat sich den Log mit der ID "' + str(
                    ctx.guild.id) + '" ausgeben lassen!', id=ctx.guild.id)
            else:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster '
                                      'Befehl ist!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(
                    user) + ' hat sich probiert den noch nicht existierenden Log mit der ID "' + str(
                    ctx.guild.id) + '" ausgeben zu lassen!', id=ctx.guild.id)

        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'serverlog im Channel #' + str(channel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()

    @botlog.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
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
                      get_prefix_string(ctx.message) + 'botlog zu nutzen.', id=ctx.guild.id)



########################################################################################################################


def setup(bot):
    bot.add_cog(botlog(bot))