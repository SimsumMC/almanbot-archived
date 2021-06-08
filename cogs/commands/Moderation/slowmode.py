import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class slowmode(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int, channel: discord.TextChannel = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            try:
                if channel is None:
                    await ctx.channel.edit(slowmode_delay=seconds)
                    channel = str(ctx.channel.mention)
                    channelname = ctx.channel.name
                else:
                    await channel.edit(slowmode_delay=seconds)
                    channel = channel.mention
                    channelname = channel.name
                embed = discord.Embed(title='**Slowmode**', colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                        '?width=676&height=676')
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name="⠀",
                                value=f'Der Slowmode vom Channel {channel} wurde zu {seconds} Sekunden geändert.')
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat im Chat "#' + str(
                    channelname) + '" den Slowmode'
                                   f' auf {seconds} Sekunden gesetzt.', id=ctx.guild.id)
            except Exception:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Bot hatte nicht die nötigen Berrechtigungen um ' +
                          get_prefix_string(ctx.message) + 'slowmode auszuführen..', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' + get_prefix_string(ctx.message) +
                      'slowmode im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @slowmode.error
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
                                  '```manage_channels```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um ' +
                      get_prefix_string(ctx.message) + 'slowmode zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'slowmode <Sekunden> <opt. Channel>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'slowmode eingegeben.', id=ctx.guild.id)
########################################################################################################################


def setup(bot):
    bot.add_cog(slowmode(bot))