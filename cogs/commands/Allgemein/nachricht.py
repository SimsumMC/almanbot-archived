import datetime
import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour, colour_check \
    , colour_check, get_colour_code


class nachricht(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nachricht(self, ctx, title, colour, channel: discord.TextChannel, *, message):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            try:
                if colour_check(colour):
                    colour = get_colour_code(colour)
                else:
                    colour = get_colour(ctx.message)
                embed = discord.Embed(title=f"**{title}**", description=message, colour=colour)
                embed.set_footer(
                    text='von ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                await channel.send(embed=embed)
                embed = discord.Embed(title='**Nachricht**', colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                        '/winging-easy.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix '
                                      + get_prefix_string(message=ctx.message)
                                 , icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                            '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎', value=f'Die Nachricht wurde erfolgreich in den Channel {channel.mention}'
                                                ' geschickt!', inline=False)
                await ctx.send(embed=embed)
                log(input=f"{time}: Der Spieler {user} hat mit dem Befehl {get_prefix_string(ctx.message)}nachricht"
                          f" eine Nachricht in #{channel} gesendet.", id=ctx.guild.id)
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
                          get_prefix_string(ctx.message) + 'nachricht auszuführen.', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'nachricht im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @nachricht.error
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
                                  get_prefix_string(ctx.message) + 'nachricht <Titel> <Farbe> <Channel> <Nachricht>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'ban eingegeben.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(nachricht(bot))
