import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions, BadArgument

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_colour, is_not_pinned


class clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        if amount < 101:
            try:
                deleted = await ctx.channel.purge(limit=amount + 1, check=is_not_pinned)
                if amount == 1:
                    nachricht = "Nachricht"
                    wurde = "wurde"
                else:
                    nachricht = "Nachrichten"
                    wurde = "wurden"
                embed = discord.Embed(title="Clear", description=f'Es {wurde} {len(deleted) - 1} {nachricht} gelöscht!',
                                      colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed, delete_after=5)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat ' + str(
                    len(deleted) - 1) + ' Nachrichten im Kanal #' +
                    str(name) + ' mit dem Befehl ' + get_prefix_string(ctx.message) + 'clear gelöscht.',
                    id=ctx.guild.id)
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
                          get_prefix_string(ctx.message) + 'clear auszuführen.', id=ctx.guild.id)

        else:
            embed = discord.Embed(title='**Fehler**',
                                  description='Du kannst nicht über 100 Nachrichten  aufeinmal löschen!'
                                              ' Nutze dazu bitte !channelclear .',
                                  colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(message=ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                      '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed, delete_after=5)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat probiert ' + str(
                amount - 1) + ' Nachrichten im Kanal #' +
                str(name) + ' mit dem Befehl ' + get_prefix_string(ctx.message) + 'clear zu löschen, hat aber das '
                                                                                  'Limit von 100 Nachrichten überschritten!',
                id=ctx.guild.id)

    @clear.error
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
                                  '```manage_messages```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um ' +
                      get_prefix_string(ctx.message) + 'clear zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'clear <Nachrichtenanzahl>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'clear eingegeben.', id=ctx.guild.id)
        if isinstance(error, BadArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(
                text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                    message=ctx.message),
                icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                         '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Bitte gib eine gültige Zahl ein, z.B ```50```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler  ' + user + ' hat beim Befehl ' +
                      get_prefix_string(ctx.message) + 'clear Buchstaben statt Zahlen angegeben.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(clear(bot))