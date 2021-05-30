import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from commands.functions import log, get_author, get_prefix_string, get_botc, get_colour, get_botname, make_qr, whoisr,\
    colour_check, get_colour_code
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from main import client


class allgemein(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            embed = discord.Embed(title='**Invites**', color=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed,
                           components=[[
                               Button(style=ButtonStyle.URL, label="Bot Invite",
                                      url="https://discord.com/oauth2/authorize?"
                                          "client_id=802922765782089738&scope=bot&permissions=2620914775"),
                               Button(style=ButtonStyle.URL, label="Discord Server",
                                      url="https://discord.visitlink.de"),
                               Button(style=ButtonStyle.URL, label="Website", url="https://communitybot.visitlink.de/"),
                           ]], )

            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl  ' +
                get_prefix_string(ctx.message) + 'invite benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'invite im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()


    @commands.command()
    async def botinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            ergebnis = 0
            for guild in client.guilds:
                ergebnis += guild.member_count
            embed = discord.Embed(title='**Botinfo**', color=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='**Entwickler**', value='SimsumMC#3579', inline=True)
            embed.add_field(name='**Projektbeginn**', value='Anfang 2021', inline=True)
            embed.add_field(name='**Arbeitszeit**', value='ca. 40 Stunden', inline=True)
            embed.add_field(name='**Server**', value=f'{len(client.guilds)}', inline=True)
            embed.add_field(name='**Nutzer**', value=f'{ergebnis}', inline=True)
            embed.add_field(name='**Source**', value='[Github](https://github.com/SimsumMC/communitybot)', inline=True)
            embed.add_field(name='**Website**', value='[Link](https://communitybot.visitlink.de/)', inline=True)
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl  ' +
                get_prefix_string(ctx.message) + 'botinfo benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'botinfo im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()


    @commands.command()
    async def qr(self, ctx, *, link):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        path = f'qrcode by {get_botname()}.png'
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            make_qr(str(path), link)
            embed = discord.Embed(title="**QR Code**", colour=get_colour(ctx.message))
            file = discord.File(path, filename="image.png")
            embed.set_image(url="attachment://image.png")
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                    '.png?width=676&height=676')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            await ctx.send(file=file, embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat mit dem Befehl !qr einen QRCODE des Links ' + str(
                link) + ' generiert!', ctx.guild.id)
            os.remove(path)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                get_prefix_string(ctx.message) + 'qr im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @qr.error
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
                                  get_prefix_string(ctx.message) + 'qr <Link>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                get_prefix_string(ctx.message) + 'qr eingegeben.', id=ctx.guild.id)


    @commands.command()
    async def ping(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        ping = round(client.latency * 1000)
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            embed = discord.Embed(title='**Ping**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            embed.add_field(name='‎', value=f'Mein  Ping beträgt aktuell {ping}ms!', inline=False)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                              '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(user) + f' hat sich den Ping ({str(ping)}ms) ausgeben lassen.'
                , id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'qr im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    async def nutzerinfo(self, ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            if member is None:
                member = ctx.author
            roles = [role for role in member.roles]

            embed = discord.Embed(title=f"**Nutzerinfo für {member}**", colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="**Nutzername:**", value=member.display_name, inline=True)
            embed.add_field(name="**ID:**", value=member.id, inline=True)

            embed.add_field(name="**Tag:**", value=member.discriminator, inline=True)
            embed.add_field(name="Aktuelle Aktivität:",
                            value=f" {member.activity.name}" if member.activity is not None else "Keine",
                            inline=True)
            embed.add_field(name="**Erstellt am:**", value=member.created_at.strftime("%d.%m.%y um %H:%M"),
                            inline=True)
            embed.add_field(name="**Beigetreten am:**", value=member.joined_at.strftime("%d.%m.%y um %H:%M"),
                            inline=True)
            embed.add_field(name=f"**Rollen ({len(roles) - 1}):**", value=" **|** "
                            .join([role.mention for role in roles if not role.is_default()]),
                            inline=True)
            embed.add_field(name="**Höchste Rolle:**", value=member.top_role.mention, inline=True)
            embed.add_field(name="**Bot?:**", value=str(whoisr(member=member)) , inline=True)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl  ' +
                get_prefix_string(ctx.message) + 'nutzerinfo benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'nutzerinfo im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    async def serverinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        bot, member = 0, 0
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            embed = discord.Embed(title=f"**Serverinfo für {ctx.guild.name}**", colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="**Name:**", value=ctx.guild.name, inline=True)
            embed.add_field(name="**ID:**", value=ctx.guild.id, inline=True)
            embed.add_field(name="**Region:**", value=ctx.guild.region, inline=True)
            embed.add_field(name="**Erstellt am:**", value=ctx.guild.created_at.strftime("%d.%m.%y um %H:%M")
                            , inline=True)
            embed.add_field(name="**Besitzer:**", value=ctx.guild.owner.mention, inline=True)
            embed.add_field(name="**Spielerzahlen:**", value=f"Gesamt: `{ctx.guild.member_count}`\n"
                                                         "Spieler: "
                                                         f"`{len(list(filter(lambda m: not m.bot,ctx.guild.members)))}`\n"
                                                         "Bots: "
                                                         f"`{len(list(filter(lambda m: m.bot, ctx.guild.members)))}`\n"
                                                         , inline=True)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl  ' +
                get_prefix_string(ctx.message) + 'serverinfo benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'serverinfo im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()


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
                embed = discord.Embed(title=f"**{title}**",description=message, colour=colour)
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
    bot.add_cog(allgemein(bot))
