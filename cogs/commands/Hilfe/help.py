import asyncio
import datetime
import discord
from discord.ext import commands

from cogs.core.functions.functions import get_botc, get_author, get_prefix_string, get_colour, log
from discord_components import Button, ButtonStyle

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["help", "commands"])
    async def hilfe(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == "None":
            await ctx.send(embed=get_page(ctx.message, ctx.author.name, "übersicht"),
                           components=[[
                               Button(style=ButtonStyle.red, label="Übersicht", emoji="🔖"),
                               Button(style=ButtonStyle.red, label="Allgemein", emoji="🤖"),
                               Button(style=ButtonStyle.red, label="Informationen", emoji="📉"),
                               Button(style=ButtonStyle.red, label="Unterhaltung", emoji="🎲")], [
                               Button(style=ButtonStyle.red, label="Moderation", emoji="🛡"),
                               Button(style=ButtonStyle.red, label="Administration", emoji="⚙")

                           ]],
                           )
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'hilfe benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'ban im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

def get_page(message, user, page):
    if page == "übersicht":
        embed = discord.Embed(title='**Hilfe Übersicht**', description='Hier findest du alle Hilfekategorien!',
                              colour=get_colour(message))
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                '.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
            get_prefix_string(message=message)),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                  '/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name=f'`{get_prefix_string(message)}hilfe`',
                        value='Zeigt dir eine Übersicht aller'
                              ' Hilfekategorien!', inline=False)
        embed.add_field(name=f'**Allgemein**',
                        value='Hier findest du ein paar nützliche Befehle!', inline=False)
        embed.add_field(name=f'**Informationen**',
                        value='Du brauchst Informationen? Hier bekommst du sie!', inline=False)
        embed.add_field(name=f'**Unterhaltung**',
                        value='Hier dreht sich alles ums Spaß haben!', inline=False)
        embed.add_field(name=f'**Moderation**',
                        value='Ob Muten oder direkt bannen - hier findest du alles was du als Moderator brauchst.'
                        , inline=False)
        embed.add_field(name=f'**Administration**',
                        value='Hier gibts noch viele Einstellungen für die Admins!', inline=False)
    elif page == "allgemein":
        embed = discord.Embed(title='**Hilfe Allgemein**',
                              description='Hier findest du alle Befehle zu der Kategorie Allgemein!',
                              colour=get_colour(message))
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                '.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
            get_prefix_string(message=message)),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                  '/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name=f'**{get_prefix_string(message)}hilfe**',
                        value='Zeigt dir eine Übersicht aller'
                              ' Hilfeseiten!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}invite**',
                        value='Invite mich oder schau bei meinem Zuhause vorbei!', inline=False)

        embed.add_field(name=f'**{get_prefix_string(message)}qr**', value='Erstelle einen QR Code zu einer'
                                                                              ' beliebigen Website!',
                        inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}avatar**',
                        value='Gebe dir das Profilbildvon einem Nutzer aus!',
                        inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}nachricht**',
                        value='Sende einen personalisierten Embed in einen Channel deiner Wahl!',
                        inline=False)
    elif page == "informationen":
        embed = discord.Embed(title='**Hilfe Informationen**',
                              description='Hier findest du alle Befehle zu der Kategorie Allgemein!',
                              colour=get_colour(message))
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                '.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
            get_prefix_string(message=message)),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                  '/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name=f'**{get_prefix_string(message)}ping**', value='Zeigt dir meinen Ping an!'
                        , inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}botinfo**',
                        value='Zeigt dir Daten zu mir!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}serverinfo**',
                        value='Zeigt Daten zum aktuellen Server an!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}nutzerinfo**',
                        value='Zeigt Daten zu einem Spieler an!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}lookup**',
                        value='Zeigt Daten zu einer angegebenen Domain an!', inline=False)
    elif page == "unterhaltung":
        embed = discord.Embed(title='**Hilfe Unterhaltung**',
                              description='Hier findest du alle Befehle zu der Kategorie Unterhaltung!',
                              colour=get_colour(message))
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                '.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
            get_prefix_string(message=message)),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                  '/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name=f'**{get_prefix_string(message)}würfel**', value='Nutze meinen integrierten'
                                                                                  ' Würfel!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}ssp**',
                        value='Spiele Schere, Stein, Papier gegen'
                              ' mich!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}meme**',
                        value='Zeigt dir einen zufälligen Meme'
                              ' von Reddit!', inline=False)
    elif page == "moderation":
        embed = discord.Embed(title='**Hilfe Moderation**',
                              description='Hier findest du alle Befehle zu der Kategorie Moderation!',
                              colour=get_colour(message))
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                '.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
            get_prefix_string(message=message)),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                  '/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name=f'**{get_prefix_string(message)}slowmode**', value=
        'Lege den Intervall zwischen Nachrichten in einem bestimmten Kanal fest.!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}clear**',
                        value='Lösche eine bestimmte Anzahl an'
                              ' Nachrichten!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}ban**',
                        value='Banne einen bestimmten Spieler bis'
                              ' er entbannt wird!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}unban**', value='Entbanne einen zuvor'
                                                                                 ' gebannten Spieler!',
                        inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}kick**',
                        value='Kicke einen bestimmten Spieler!'
                        , inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}mute**', value=
        'Stumme einen spezifischen Spieler!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}unmute**', value=
        'Entstumme einen spezifischen Spieler!', inline=False)
    elif page == "administration":
        embed = discord.Embed(title='**Hilfe Administration**',
                              description='Hier findest du alle Befehle zu der Kategorie Administrator!',
                              colour=get_colour(message))
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                '.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
            get_prefix_string(message=message)),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                  '/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name=f'**{get_prefix_string(message)}config hilfe**', value='Ändere die'
                                                                                        ' Botkonfiguration über einen Befehl!',
                        inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}channelclear**',
                        value='Lösche alle Nachrichten'
                              ' aus einem Channel!', inline=False)
        embed.add_field(name=f'**{get_prefix_string(message)}botlog**', value='Gebe dir den Botlog deines'
                                                                                  ' Servers aus!', inline=False)
    return embed



########################################################################################################################


def setup(bot):
    bot.add_cog(help(bot))
