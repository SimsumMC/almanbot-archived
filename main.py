import discord
import qrcode
import random
import json
import asyncio
import discord.member
import datetime
import os
import praw
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, MissingRequiredArgument
from discord import *

filename = 'config.json'


with open(filename) as json_file:
    data = json.load(json_file)
Token = data['Token']
Prefix = data['Prefix']
Name = data['Name']
Author = data['Author']
memechannel = data['memechannel']
botchannel = data['botchannel']
json_file.close()

client = commands.Bot(command_prefix=commands.when_mentioned_or(Prefix), intents=discord.Intents.all())


def is_not_pinned(message):
    return not message.pinned


def make_qr(filename, msg):
    img = qrcode.make(msg)
    img.save(filename)


@client.event
async def on_ready():
    print('Der {} Bot wurde erfolgreich gestartet!'.format(Name))
    while True:
        await client.change_presence(activity=discord.Game('discord.visitlink.de'), status=discord.Status.online)
        await asyncio.sleep(2.5)
        await client.change_presence(activity=discord.Game('!hilfe'), status=discord.Status.online)
        await asyncio.sleep(2.5)
        with open(filename) as json_file:
            data = json.load(json_file)
        global memechannel
        memechannel = data['memechannel']
        global botchannel
        botchannel = data['botchannel']
        json_file.close()


@client.command(aliases=['hilfe', 'Hilfe'])
async def __Hilfe(ctx, *, page=None):
    time = datetime.datetime.now()
    user = ctx.author.name
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        if page is None:
            embed = discord.Embed(title='Hilfe Übersicht', description='Hier findest du alle Hilfeseiten!', colour=13372193)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='!hilfe', value='Zeigt dir eine Übersicht aller Hilfeseiten!', inline=False)
            embed.add_field(name='!hilfe Allgemein', value='Zeigt dir alle Befehle der Kategorie Allgemein an!', inline=False)
            embed.add_field(name='!hilfe Unterhaltung', value='Zeigt dir alle Befehle der Kategorie Unterhaltung an!', inline=False)
            embed.add_field(name='!hilfe Moderation', value='Zeigt dir alle Befehle der Kategorie Moderation an!', inline=False)
            embed.add_field(name='!hilfe Administration', value='Zeigt dir alle Befehle der Kategorie Administrator an!',inline=False)
            await ctx.channel.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !hilfe benutzt!')
        elif page == 'allgmein' or page == 'Allgemein' or page == 'all':
            embed = discord.Embed(title='Hilfe Allgemein', description='Hier findest du alle Befehle zu der Kategorie Allgemein!', colour=13372193)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='!hilfe', value='Zeigt dir eine Übersicht aller Hilfeseiten!', inline=False)
            embed.add_field(name='!qr', value='Erstelle einen QR Code zu einer beliebigen Website!', inline=False)
            embed.add_field(name='!invite', value='Schau bei meinem Zuhause vorbei!', inline=False)
            embed.add_field(name='!ping', value='Zeigt dir meinen Ping an!', inline=False)
            await ctx.channel.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !hilfe Allgemnein benutzt!')
        elif page == 'Unterhaltung' or page == 'unterhaltung' or page == 'fun':
            embed = discord.Embed(title='Hilfe Unterhaltung', description='Hier findest du alle Befehle zu der Kategorie Unterhaltung!', colour=13372193)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='!würfel', value='Nutze meinen integrierten Würfel!', inline=False)
            embed.add_field(name='!ssp', value='Spiele Schere, Stein, Papier gegen mich!', inline=False)
            embed.add_field(name='!meme', value='Zeigt dir einen zufälligen Meme von Reddit!', inline=False)
            await ctx.channel.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !hilfe Unterhaltung benutzt!')
        elif page == 'Moderation' or page == 'moderation' or page == 'mod':
            embed = discord.Embed(title='Hilfe Moderation', description='Hier findest du alle Befehle zu der Kategorie Moderation!',colour=13372193)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='!clear', value='Lösche eine bestimmte Anzahl an Nachrichten!', inline=False)
            embed.add_field(name='!ban', value='Banne einen bestimmten Spieler bis er entbannt wird!', inline=False)
            embed.add_field(name='!unban', value='Entbanne einen zuvor gebannten SPieler!', inline=False)
            embed.add_field(name='!kick', value='Kicke einen bestimmten Spieler!', inline=False)
            await ctx.channel.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !hilfe Administration benutzt!')
        elif page == 'Administration' or page == 'administration' or page == 'admin' or page == 'Admin':
            embed = discord.Embed(title='Hilfe Administration', description='Hier findest du alle Befehle zu der Kategorie Administrator!',colour=13372193)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='!config hilfe', value='Ändere die Botkonfiguration über einen Befehl!', inline=False)
            embed.add_field(name='!channelclear', value='Lösche alle Nachrichten aus einem Channel!', inline=False)
            await ctx.channel.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !hilfe Administation benutzt!')
        else:
            embed = discord.Embed(colour=13372193)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='Fehler',
                            value='Die Hilfeseite ist ungültig, nutze !hilfe um die unterschiedlichen Seiten anzuzeigen!',
                            inline=False)
            await ctx.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat eine ungültige Seitte beim Befehl !hilfe angegeben.')
    else:
        msg = await ctx.send('Du kannst diesen Befehl nur im #' + str(botchannel) + ' Chat nutzen!')
        await asyncio.sleep(3)
        await msg.delete()
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !hilfe im Channel #' + str(name) + ' zu benutzen!')


@client.command(aliases=['config', 'Config', 'edit', 'Edit'])
async def __Config(ctx, config=None, config2=None):
    time = datetime.datetime.now()
    user = ctx.author.name
    if config == 'hilfe':
        embed = discord.Embed(title='Config Hilfe', description='Hier findest du alle Subbefehle zum !config Befehl!', colour=13372193)
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='!config name/Name <name> ', value='Ändere den Namen deines Bots, der in der Konsole angezeigt wird!',inline=False)
        embed.add_field(name='!config prefix/Prefix <name> ', value='Ändere den Prefix deines Bots, der in der Konsole angezeigt wird!', inline=False)
        embed.add_field(name='!config token/Token <name> ', value='Ändere den Token deines Bots, auf dem das Skript gestartet wird.!', inline=False)
        embed.add_field(name='!config botchannel/Botchannel <name / "None"> ', value='Sorge dafür das die befehle nur in einem bestimmten Kanal funktionieren!', inline=False)
        embed.add_field(name='!config memechannel/Memechannel <name / "None"> ', value='Sorge dafür das der Memes befehl nur in einem bestimmten Kanal funktioniert!', inline=False)
        await ctx.send(embed=embed)
        print(str(time) + ': Der Spieler ' + str(user) + ' hat den Command !config hilfe benutzt!')
    elif config == 'botchannel' or config == 'Botchannel':
        if config2 == 'None':
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
            data['botchannel'] = config2
            os.remove(filename)
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            await ctx.send('Du hast erfolgreich den festgelegten Botkanal gelöscht. Es kann ein paar Sekunden in Anspruch nehmen, bis es sich aktualisiert.')
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den festgelegten Botkanal gelöscht.')
        else:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
            data['botchannel'] = config2
            os.remove(filename)
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            await ctx.send('Du hast erfolgreich das Modul "' + str(config) + '" zu ' + str(config2) + ' geändert. Es kann ein paar Sekunden in Anspruch nehmen, bis es sich aktualisiert.')
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Kanal #' + str(config2) + ' zum Botkanal festgelegt.')
    elif config == 'memechannel' or config == 'Memechannel':
        if config2 == 'None':
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
            data['memechannel'] = config2
            os.remove(filename)
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            await ctx.send('Du hast erfolgreich den festgelegten Memekanal gelöscht. Es kann ein paar Sekunden in Anspruch nehmen, bis es sich aktualisiert.')
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den festgelegten Memekanal gelöscht.')
        else:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
            data['memechannel'] = config2
            os.remove(filename)
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            await ctx.send('Du hast erfolgreich das Modul "' + str(config) + '" zu ' + str(config2) + ' geändert. Es kann ein paar Sekunden in Anspruch nehmen, bis es sich aktualisiert.')
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Kanal #' + str(config2) + ' zum Memekanal festgelegt.')
    elif config == 'prefix' or config == 'Prefix':
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        data['Prefix'] = config2
        os.remove(filename)
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        await ctx.send('Du hast erfolgreich das Modul "' + str(config) + '" zu ' + str(config2) + ' geändert. Um die Änderungen zu übernehmen, starte bitte den Bot neu!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hat den Prefix zu "' + str(config2) + '" geändert.')
    elif config == 'name' or config == 'Name':
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        data['Name'] = config2
        os.remove(filename)
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        await ctx.send('Du hast erfolgreich das Modul "' + str(config) + '" zu ' + str(config2) + ' geändert. Um die Änderungen zu übernehmen, starte bitte den Bot neu!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hat den Botnamen zu "' + str(config2) + '" geändert.')
    elif config == 'token' or config == 'token':
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        data['Token'] = config2
        os.remove(filename)
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        msg = await ctx.send('Du hast erfolgreich das Modul "' + str(config) + '" zu ' + str(config2)[:2] +'... geändert. Um die Änderungen zu übernehmen, starte bitte den Bot neu!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hat den Prefix zu "' + str(config2) + '" geändert.')
        await msg.pin()
        await ctx.channel.purge(limit=3, check=is_not_pinned)
        await asyncio.sleep(3)
        await msg.unpin()

@client.command(aliases=['inv', 'invite', 'Invite'])
async def __INVITE(message):
    time = datetime.datetime.now()
    user = message.author.name
    embed = discord.Embed(title='**Invite**', colour=13372193)
    embed.set_footer(text='for ' + str(user) + ' | by '+ str(Author) +' | Prefix ' + str(Prefix),
                     icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
    embed.add_field(name='‎', value='Link: https://discord.visitlink.de', inline=False)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
    await message.channel.send(embed=embed)
    print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !invite benutzt!')


@client.command(aliases=['ssp', 'SSP', 'SchereSteinPapier', 'scheresteinpapier'])
async def __SSP(message):
    time = datetime.datetime.now()
    user = message.author.name
    embed = discord.Embed(colour=13372193)
    embed.set_footer(text='for ' + str(user) + ' | by '+ str(Author) +' | Prefix ' + str(Prefix), icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
    embed.add_field(name='**Schere Stein Papier**', value='Lass uns "Schere Stein Papier" spielen! Nutze dazu die Commands:', inline=False)
    embed.add_field(name='!schere', value='Spiele die Schere aus!', inline=False)
    embed.add_field(name='!stein', value='Spiele den Stein aus!', inline=False)
    embed.add_field(name='!papier', value='Spiele das Papier aus!', inline=False)
    await message.channel.send(embed=embed)
    print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !ssp benutzt!')


@client.command(aliases=['schere', 'Schere'])
async def __SCHERE(message):
    time = datetime.datetime.now()
    user = message.author.name
    schere = ['Ich hatte auch die Schere, Unentschieden!',
              'Du hast gewonnen, ich hatte mich für das Papier entschieden!',
              'Guter Versuch, aber ich habe aber mit dem Stein gewonnen!']
    schererandom = random.choice(schere)
    embed = discord.Embed(title='Schere Stein Papier', colour=13372193)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
    embed.set_footer(text='for ' + str(user) + ' | by '+ str(Author) +' | Prefix ' + str(Prefix),
                     icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
    embed.add_field(name='‎', value='‎ ' + str(schererandom) + ' ‎', inline=False)
    await message.channel.send(embed=embed)
    print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !schere benutzt!')


@client.command(aliases=['Stein', 'stein'])
async def __STEIN(message):
    time = datetime.datetime.now()
    user = message.author.name
    stein = ['Ich hatte auch den Stein, Unentschieden!', 'Du hast gewonnen, ich hatte mich für die Schere entschieden!',
             'Guter Versuch, aber ich habe aber mit dem Papier gewonnen!']
    steinrandom = random.choice(stein)
    embed = discord.Embed(title='Schere Stein Papier', colour=13372193)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
    embed.set_footer(text='for ' + str(user) + ' | by '+ str(Author) +' | Prefix ' + str(Prefix),
                     icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
    embed.add_field(name='‎', value='‎ ' + str(steinrandom) + ' ‎', inline=False)
    await message.channel.send(embed=embed)
    print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !stein benutzt!')


@client.command(aliases=['Papier', 'papier'])
async def __PAPIER(message):
    time = datetime.datetime.now()
    user = message.author.name
    papier = ['Ich hatte auch das Papier, Unentschieden!',
              'Du hast gewonnen, ich hatte mich für den Stein entschieden!',
              'Guter Versuch, aber ich habe aber mit der Schere gewonnen! Papier ist leider nur so dünn...']
    papierrandom = random.choice(papier)
    embed = discord.Embed(title='Schere, Stein, Papier', colour=13372193)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png')
    embed.set_footer(text='for ' + str(user) + ' | by '+ str(Author) +' | Prefix ' + str(Prefix),
                     icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
    embed.add_field(name='‎', value='‎ ' + str(papierrandom) + ' ‎', inline=False)
    await message.channel.send(embed=embed)
    print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !papier benutzt!')


@client.command(aliases=['CLEAR', 'clear', 'c'])
@commands.has_permissions(manage_messages=True)
async def __CLEAR(ctx, amount=-1):
    time = datetime.datetime.now()
    user = ctx.author.name
    channeln = ctx.channel.name
    if amount == -1:
        msg = await ctx.send('Du musst eine Anzahl an Nachrichten eingeben, also !qr "Hier einen Link"')
        print(str(time) + ': Der Spieler ' + str(user) + ' hatte Probleme mit dem Befehl !clear.')
        await asyncio.sleep(3)
        await msg.delete()
    elif amount == 1:
        await ctx.channel.purge(limit=amount + 1, check=is_not_pinned)
        msg = await ctx.channel.send('Es wurden eine Nachricht gelöscht!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hat eine Nachrichten im Kanal #' + str(channeln) +' mit dem Befehl !clear gelöscht.')
        await asyncio.sleep(3)
        await msg.delete()
    elif amount > 100:
        await ctx.channel.send('Du kannst nicht über 100 Nachrichten löschen! Wenn du alle Nachrichten aus #' + str(channeln) + ' löschen willst, nutze !channelclear.')
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert ' + str(amount) + ' im Kanal #' + str(channeln) + ' an Nachrichten mit dem Befehl !clear zu löschen, hat aber das Limit überschritten.')
    else:
        await ctx.channel.purge(limit=amount + 1, check=is_not_pinned)
        msg = await ctx.channel.send('Es wurden ' + str(amount) + ' Nachrichten gelöscht!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hat ' + str(amount) + ' Nachrichten im Kanal #' + str(channeln) + ' mit dem Befehl !clear gelöscht.')
        await asyncio.sleep(3)
        await msg.delete()

@__CLEAR.error
async def handle_error(ctx, error):
    time = datetime.datetime.now()
    user = ctx.author.name
    if isinstance(error, MissingPermissions):
        await ctx.send('Du hast nicht die nötigen Berrechtigungen um den Befehl !clear zu nutzen!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hatte nicht die nötigen Berrechtigungen gehabt um !clear zu nutzen.')


@client.command(aliases=['channelclear', 'Channelclear'])
@commands.has_permissions(administrator=True)
async def __CHANNELCLEAR(ctx):
    channelid = ctx.channel.id
    channel1 = client.get_channel(channelid)
    time = datetime.datetime.now()
    user = ctx.author.name
    await channel1.clone()
    await channel1.delete()
    # channelname = int(''.join(i for i in channel1 if i.isdigit()))
    # channel2 = client.get_channel(channelname)
    # await channel2.channel.send('Der Kanal wurde erfolgreich gecleart!')
    print(str(time) + ': Der Spieler ' + str(user) + ' hat den Chat "#' + str(channel1) + '" gecleart.')


@__CHANNELCLEAR.error
async def handle_error(ctx, error):
    time = datetime.datetime.now()
    user = ctx.author.name
    if isinstance(error, MissingPermissions):
        await ctx.send('Du hast nicht die nötigen Berrechtigungen um den Befehl !channelclear zu nutzen!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hatte nicht die nötigen Berrechtigungen gehabt um !clear zu nutzen.')


@client.command(aliases=['qr', 'qrcode', 'qrcreate', 'qrc', 'QR', 'Qr'])
async def __QR(ctx, link=None):
    time = datetime.datetime.now()
    user = ctx.author.name
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        if link is None:
            await ctx.send('Du musst einen Link eingeben, also !qr "Hier einen Link"')
            print(str(time) + ': Der Spieler ' + str(user) + ' hatte Probleme mit dem Befehl !qr.')
        else:
            FileName = 'qrcode by {}.png'.format(Name)
            make_qr(FileName, link)
            await ctx.send(file=discord.File('qrcode by {}.png'.format(Name)))
            print(str(time) + ': Der Spieler ' + str(user) + ' hat mit dem Befehl !qr einen QRCODE des Links ' + str(link) + ' generiert!')
            os.remove('qrcode by {}.png'.format(Name))
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !ping im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@client.command(aliases=['meme', 'memes', 'Meme', 'Memes'])
async def __Meme(ctx):
    time = datetime.datetime.now()
    user = ctx.author.name
    name = ctx.channel.name
    if name == memechannel or memechannel == 'None':
        reddit = praw.Reddit(client_id='JiHoJGCPBC9vlg',
                             client_secret='egXFBVdIx7ucn9_6tji18kyLClWCIA',
                             user_agent='Test Meme Bot',
                             check_for_async=False)

        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(title=submission.title, colour=13372193)
        embed.set_image(url=submission.url)
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("<:animatedheart:815519733474000957>")
        print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !meme benutzt!')
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(memechannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !meme im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@client.command(aliases=['ping', 'Ping'])
async def __PING(ctx):
    time = datetime.datetime.now()
    user = ctx.author.name
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        ping = round(client.latency * 1000)
        embed = discord.Embed(title='Ping', colour=13372193)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='‎', value='Mein Ping beträgt ' + str(ping) + 'ms !', inline=False)
        await ctx.send(embed=embed)
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !ping im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@client.command(aliases=['würfel', 'Würfel'])
async def __WÜRFEL(ctx):
    time = datetime.datetime.now()
    user = ctx.author.name
    name = ctx.channel.name
    value = random.randint(1, 6)
    if name == botchannel or botchannel == 'None':
        embed = discord.Embed(title='Würfel', colour=13372193)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/645276319311200286/803550939112931378/wurfelv2.png')
        embed.set_footer(text='for ' + str(user) + ' | by SidsonMC#1524 | Prefix !',
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='‎', value='Du hast eine ' + str(value) + ' gewürfelt!', inline=False)
        await ctx.send(embed=embed)
        print(str(time) + ': ' + str(user) + ' hat eine ' + str(value) + ' gewürfelt.')
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !würfel im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@client.command(aliases=['ban', 'Ban'])
@commands.has_permissions(ban_members=True)
async def __BAN(ctx, member: discord.Member, *, reason=None):
    time = datetime.datetime.now()
    user = ctx.author.name
    userm = ctx.author.mention
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        embed = discord.Embed(title='Ban', colour=13372193)
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Moderator:', value=userm, inline=False)
        embed.add_field(name='Nutzer:', value=str(member), inline=False)
        embed.add_field(name='Grund:', value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.ban(reason=reason)
        print(str(time) + ': Der Moderator ' + str(user) + 'hat den Nutzer ' + str(member) + ' erfolgreich für "' + str(reason) + '" gebannt.')
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !ban im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@__BAN.error
async def handle_error(ctx, error):
    time = datetime.datetime.now()
    user = ctx.author.name
    if isinstance(error, MissingPermissions):
        await ctx.send('Du hast nicht die nötigen Berrechtigungen um den Befehl !ban zu nutzen!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hatte nicht die nötigen Berrechtigungen gehabt um !ban zu nutzen.')
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(colour=13372193)
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Fehler', value='Bitte tagge einen Nutzer den du bannen willst, z.B. !ban @Spieler#1234', inline=False)
        await ctx.send(embed=embed)
        print(str(time) + ': Der Spieler ' + str(user) + ' hat keinen Spieler beim Befehl !ban angegeben.')


@client.command(aliases=['unban', 'Unban', 'pardon', 'Pardon'])
@commands.has_permissions(ban_members=True)
async def __UNBAN(ctx, *, member):
    time = datetime.datetime.now()
    user = ctx.author.name
    userm = ctx.author.mention
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for ban_entry in banned_users:
            user2 = ban_entry.user

            if (user2.name, user2.discriminator) == (member_name, member_disc):
                embed = discord.Embed(title='Unban', colour=13372193)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
                embed.add_field(name='Moderator:', value=userm, inline=False)
                embed.add_field(name='Nutzer:', value=str(member), inline=False)
                await ctx.send(embed=embed)
                await ctx.guild.unban(user2)
                print(str(time) + ': Der Moderator ' + str(user) + ' hat den Nutzer ' + str(member) + ' erfolgreich entbannt.')
                return
            else:
                print('failed')
        embed = discord.Embed(colour=13372193)
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Fehler',
                        value='Der Nutzer ' + str(member) + ' taucht nicht in der Liste der gebannten Leute auf.',
                        inline=False)
        await ctx.send(embed=embed)
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !unban im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@__UNBAN.error
async def handle_error(ctx, error):
    time = datetime.datetime.now()
    user = ctx.author.name
    if isinstance(error, MissingPermissions):
        await ctx.send('Du hast nicht die nötigen Berrechtigungen um den Befehl !ban zu nutzen!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hatte nicht die nötigen Berrechtigungen gehabt um !ban zu nutzen.')
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(colour=13372193)
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Fehler', value='Bitte tagge einen Nutzer den du bannen willst, z.B. !ban @Spieler#1234', inline=False)
        await ctx.send(embed=embed)
        print(str(time) + ': Der Spieler ' + str(user) + ' hat keinen Spieler beim Befehl !ban angegeben.')


@client.command(aliases=['kick', 'Kick'])
@commands.has_permissions(ban_members=True)
async def __KICK(ctx, member: discord.Member, *, reason=None):
    time = datetime.datetime.now()
    user = ctx.author.name
    userm = ctx.author.mention
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        embed = discord.Embed(title='Kick', colour=13372193)
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Moderator:', value=userm, inline=False)
        embed.add_field(name='Nutzer:', value=str(member), inline=False)
        embed.add_field(name='Grund:', value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.kick(reason=reason)
        print(str(time) + ': Der Moderator ' + str(user) + 'hat den Nutzer ' + str(member) + 'erfolgreich für den Grund "' + str(reason) + '"gekickt.')
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !kick im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@__KICK.error
async def handle_error(ctx, error):
    time = datetime.datetime.now()
    user = ctx.author.name
    if isinstance(error, MissingPermissions):
        await ctx.send('Du hast nicht die nötigen Berrechtigungen um den Befehl !kick zu nutzen!')
        print(str(time) + ': Der Spieler ' + str(user) + ' hatte nicht die nötigen Berrechtigungen gehabt um !kick zu nutzen.')
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(colour=13372193)
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Fehler', value='Bitte tagge einen Nutzer den du kicken willst, z.B. !kick @Spieler#1234 (Grund)', inline=False)
        await ctx.send(embed=embed)
        print(str(time) + ': Der Spieler ' + str(user) + ' hat keinen Spieler beim Befehl !kick angegeben.')


@client.command(aliases=['server', 'Server', 'mode', 'Modus', 'modus'])
async def __SERVER(ctx, modi):
    time = datetime.datetime.now()
    user = ctx.author.name
    name = ctx.channel.name
    if name == botchannel or botchannel == 'None':
        if modi == 'hilfe' or modi == 'Hilfe':
            embed = discord.Embed(title='Übersicht zu !server / !modus', colour=13372193)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='!server hilfe', value='Zeigt dir eine Übersicht zum !server Befehl!', inline=False)
            embed.add_field(name='!server top', value='Zeigt dir eine Liste der Top 10 Server an mit zugehörigen Highlits!', inline=False)
            embed.add_field(name='!server liste', value='Zeigt dir eine Liste aller eingetragenen Server mit zugehörigen Highlights.', inline=False)
            await ctx.send(embed=embed)
            print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !server hilfe benutzt!')
        if modi == 'top' or modi == 'Top':
            pass
            #embed = discord.Embed(title='Übersicht zu !server / !modus', colour=13372193)
            #embed.set_thumbnail(
                #url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            #embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                             #icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
            #embed.add_field(name='#1 GommeHD.net', value='Zeigt dir eine Übersicht zum !server Befehl!', inline=False)
            #embed.add_field(name='#2 ', value='Zeigt dir eine Liste der Top 10 Server an mit zugehörigen Highlits!', inline=False)
            #embed.add_field(name='!server liste', value='Zeigt dir eine Liste aller eingetragenen Server mit zugehörigen Highlights.', inline=False)
            #await ctx.send(embed=embed)
            #print(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !server top benutzt!')
    else:
        msg = await ctx.send('Dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel))
        print(str(time) + ': Der Spieler ' + str(user) + ' hat probiert den Befehl !server im Channel #' + str(name) + ' zu benutzen!')
        await asyncio.sleep(3)
        msg.delete()


@__SERVER.error
async def handle_error(ctx, error):
    time = datetime.datetime.now()
    user = ctx.author.name
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(colour=13372193)
        embed.set_footer(text='for ' + str(user) + ' | by ' + str(Author) + ' | Prefix ' + str(Prefix),
                         icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png?width=676&height=676')
        embed.add_field(name='Fehler', value='Bitte gebe einen Modus oder "Liste" als Argument ein, z.B. !server top / hilfe.', inline=False)
        await ctx.send(embed=embed)
        print(str(time) + ': Der Spieler ' + str(user) + ' hat keinen Modus beim Befehl !kick angegeben.')
    else:
        raise error

client.run(Token)
