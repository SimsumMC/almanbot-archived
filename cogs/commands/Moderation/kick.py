import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class kick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == 'None':
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(title='**Kick**', colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                        '?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' +
                                      get_prefix_string(message=ctx.message),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                          '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Moderator:', value=mention, inline=False)
                embed.add_field(name='Nutzer:', value=str(member), inline=False)
                embed.add_field(name='Grund:', value=reason, inline=False)
                await ctx.send(embed=embed)
                log(str(time) + ': Der Moderator ' + str(user) + 'hat den Nutzer ' + str(
                    member) + 'erfolgreich für den Grund "' + str(reason) + '"gekickt.', id=ctx.guild.id)
                return
            except Exception:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Bot hatte nicht die nötigen Berrechtigungen um ' +
                          get_prefix_string(ctx.message) + 'kick auszuführen..', id=ctx.guild.id)
                return
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' + get_prefix_string(ctx.message) +
                      'unban im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @kick.error
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
                            value='Dir fehlt folgende Berrechtigung um den Befehl auszuführen: '
                                  '```kick_members```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um ' +
                      get_prefix_string(ctx.message) + 'kick zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'kick <@Spieler>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'kick eingegeben.', id=ctx.guild.id)
########################################################################################################################


def setup(bot):
    bot.add_cog(kick(bot))