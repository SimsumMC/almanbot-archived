import asyncio
import datetime
import discord
from discord.ext import commands

from commands.functions import get_botc, get_author, get_prefix_string, get_colour
from commands.functions import log


class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hilfe(self, ctx, *, page=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            if page is None:
                embed = discord.Embed(title='Hilfe Übersicht', description='Hier findest du alle Hilfeseiten!',
                                      colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='!hilfe', value='Zeigt dir eine Übersicht aller Hilfeseiten!', inline=False)
                embed.add_field(name='!hilfe Allgemein', value='Zeigt dir alle Befehle der Kategorie Allgemein an!',
                                inline=False)
                embed.add_field(name='!hilfe Unterhaltung',
                                value='Zeigt dir alle Befehle der Kategorie Unterhaltung an!', inline=False)
                embed.add_field(name='!hilfe Moderation', value='Zeigt dir alle Befehle der Kategorie Moderation an!',
                                inline=False)
                embed.add_field(name='!hilfe Administration',
                                value='Zeigt dir alle Befehle der Kategorie Administrator an!', inline=False)
                await ctx.channel.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                    get_prefix_string(ctx.message) + 'hilfe benutzt!', ctx.guild.id)
            elif page == 'allgmein' or page == 'Allgemein' or page == 'all':
                embed = discord.Embed(title='Hilfe Allgemein',
                                      description='Hier findest du alle Befehle zu der Kategorie Allgemein!',
                                      colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='!hilfe', value='Zeigt dir eine Übersicht aller Hilfeseiten!', inline=False)
                embed.add_field(name='!qr', value='Erstelle einen QR Code zu einer beliebigen Website!', inline=False)
                embed.add_field(name='!invite', value='Schau bei meinem Zuhause vorbei!', inline=False)
                embed.add_field(name='!ping', value='Zeigt dir meinen Ping an!', inline=False)
                await ctx.channel.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                    get_prefix_string(ctx.message) + 'hilfe Allgemein benutzt!',
                    ctx.guild.id)
            elif page == 'Unterhaltung' or page == 'unterhaltung' or page == 'fun':
                embed = discord.Embed(title='Hilfe Unterhaltung',
                                      description='Hier findest du alle Befehle zu der Kategorie Unterhaltung!',
                                      colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='!würfel', value='Nutze meinen integrierten Würfel!', inline=False)
                embed.add_field(name='!ssp', value='Spiele Schere, Stein, Papier gegen mich!', inline=False)
                embed.add_field(name='!meme', value='Zeigt dir einen zufälligen Meme von Reddit!', inline=False)
                await ctx.channel.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                    get_prefix_string(ctx.message) + 'hilfe Unterhaltung benutzt!',
                    ctx.guild.id)
            elif page == 'Moderation' or page == 'moderation' or page == 'mod':
                embed = discord.Embed(title='Hilfe Moderation',
                                      description='Hier findest du alle Befehle zu der Kategorie Moderation!',
                                      colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='!clear', value='Lösche eine bestimmte Anzahl an Nachrichten!', inline=False)
                embed.add_field(name='!ban', value='Banne einen bestimmten Spieler bis er entbannt wird!', inline=False)
                embed.add_field(name='!unban', value='Entbanne einen zuvor gebannten SPieler!', inline=False)
                embed.add_field(name='!kick', value='Kicke einen bestimmten Spieler!', inline=False)
                await ctx.channel.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                    get_prefix_string(ctx.message) + 'hilfe Administration benutzt!',
                    ctx.guild.id)
            elif page == 'Administration' or page == 'administration' or page == 'admin' or page == 'Admin':
                embed = discord.Embed(title='Hilfe Administration',
                                      description='Hier findest du alle Befehle zu der Kategorie Administrator!',
                                      colour=get_colour(ctx.message))
                embed.set_thumbnail(
                    url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                        '.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='!config hilfe', value='Ändere die Botkonfiguration über einen Befehl!',
                                inline=False)
                embed.add_field(name='!channelclear', value='Lösche alle Nachrichten aus einem Channel!', inline=False)
                embed.add_field(name='!botlog', value='Gebe dir den Botlog deines Servers aus!', inline=False)
                await ctx.channel.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                    get_prefix_string(ctx.message) + 'hilfe Administation benutzt!',
                    ctx.guild.id)
            else:
                embed = discord.Embed(colour=get_colour(ctx.message))
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='Fehler',
                                value='Die Hilfeseite ist ungültig, nutze !hilfe um die unterschiedlichen Seiten '
                                      'anzuzeigen!',
                                inline=False)
                await ctx.send(embed=embed)
                log(str(time) + ': Der Spieler ' + str(
                    user) + ' hat eine ungültige Seite beim Befehl  ' +
                    get_prefix_string(ctx.message) + 'hilfe angegeben.', ctx.guild.id)
        else:
            msg = await ctx.send('Du kannst diesen Befehl nur im #' + str(botchannel) + ' Chat nutzen!')
            await asyncio.sleep(3)
            await msg.delete()
            log(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'hilfe im Channel #' + str(
                name) + ' zu benutzen!', ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(help(bot))
