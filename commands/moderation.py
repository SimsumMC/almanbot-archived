import datetime
import discord
import os
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions, BotMissingPermissions
from commands.functions import log, get_author, get_prefix_string, get_botc, get_colour, is_not_pinned, get_blacklist\
    , writejson


class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if amount < 101:
            try:
                deleted = await ctx.channel.purge(limit=amount + 1, check=is_not_pinned)
                embed = discord.Embed(description='Es wurden ' + str(deleted - 1) + ' Nachrichten gelöscht!',
                                      colour=get_colour(ctx.message))
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                    get_prefix_string(message=ctx.message)),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286'
                    '/803322491480178739/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed, delete_after=5)
                log(str(time) + ': Der Spieler ' + str(user) + ' hat ' + str(deleted - 1) + ' Nachrichten im Kanal #' +
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
                'Limit von 100 Nachrichten überschritten!', id=ctx.guild.id)

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
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            try:
                await member.ban(reason=reason)
                embed = discord.Embed(title='**Ban**', colour=get_colour(ctx.message))
                embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Moderator:', value=mention, inline=False)
                embed.add_field(name='Nutzer:', value=str(member), inline=False)
                embed.add_field(name='Grund:', value=reason, inline=False)
                await ctx.send(embed=embed)
                log(str(time) + ': Der Moderator ' + str(user) + 'hat den Nutzer ' + str(
                member) + ' erfolgreich für "' + str(reason) + '" gebannt.', id=ctx.guild.id)
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
                          get_prefix_string(ctx.message) + 'ban auszuführen.', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'ban im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @ban.error
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
                      get_prefix_string(ctx.message) + 'ban zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'ban <@Spieler> <opt. Grund>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'ban eingegeben.', id=ctx.guild.id)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == 'None':
            banned_users = await ctx.guild.bans()
            member_name, member_disc = member.split('#')
            for ban_entry in banned_users:
                user2 = ban_entry.user
                if (user2.name, user2.discriminator) == (member_name, member_disc):
                    try:
                        await ctx.guild.unban(user2)
                        embed = discord.Embed(title='**Unban**', colour=get_colour(ctx.message))
                        embed.set_thumbnail(
                        url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging'
                            '-easy.png?width=676&height=676')
                        embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                        embed.add_field(name='Moderator:', value=mention, inline=False)
                        embed.add_field(name='Nutzer:', value=str(member), inline=False)
                        await ctx.send(embed=embed)
                        log(str(time) + ': Der Moderator ' + str(user) + 'hat den Nutzer ' + str(
                        member) + ' erfolgreich entbannt.', id=ctx.guild.id)
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
                                  get_prefix_string(ctx.message) + 'unban auszuführen..', id=ctx.guild.id)
                else:
                    embed = discord.Embed(title='**Fehler**',
                                          description='Der Nutzer ' + str(member) + ' ist nicht gebannt und kann daher '
                                                                                    'auch nicht entbannt werden.',
                                          colour=get_colour(ctx.message))
                    embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                    await ctx.send(embed=embed)
                    log(str(time) + ': Der Moderator ' + str(user) + 'hat versucht den  ungültigen Nutzer ' + str(
                        member) + ' zu entbannen.', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'unban im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @unban.error
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
                      get_prefix_string(ctx.message) + 'unban zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'unban <Spieler#1234>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'unban eingegeben.', id=ctx.guild.id)

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
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Moderator:', value=mention, inline=False)
                embed.add_field(name='Nutzer:', value=str(member), inline=False)
                embed.add_field(name='Grund:', value=reason, inline=False)
                await ctx.send(embed=embed)
                log(str(time) + ': Der Moderator ' + str(user) + 'hat den Nutzer ' + str(
                member) + 'erfolgreich für den Grund "' + str(reason) + '"gekickt.', id=ctx.guild.id)
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
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
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


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int , channel: discord.TextChannel =None):
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
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
                embed.add_field(name="⠀", value=f'Der Slowmode vom Channel {channel} wurde zu {seconds} Sekunden geändert.')
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat im Chat "#' + str(channelname) + '" den Slowmode'
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
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name= 'Muted')
        if name == botchannel or botchannel == "None":
            try:
                if not mutedrole:
                    mutedrole = await guild.create_role(name="Muted")
                    for channel in guild.channels:
                        for channel in guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False,
                                                      read_message_history=True, read_messages=False)
                await member.add_roles(mutedrole, reason=reason)
                embed = discord.Embed(title='**Mute**', colour=get_colour(ctx.message))
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Moderator',
                            value=str(mention), inline=False)
                embed.add_field(name='Spieler',
                            value=str(member.mention), inline=False)
                embed.add_field(name='Grund',
                            value=str(reason), inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + f": Der Moderator {user} hat den Spieler {member} für {reason} gemuted."
                , id= ctx.guild.id)
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
                          get_prefix_string(ctx.message) + 'mute auszuführen..', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' + get_prefix_string(ctx.message) +
                'mute im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @mute.error
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
                      get_prefix_string(ctx.message) + 'mute zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'mute <@Spieler> <opt. Grund>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'mute eingegeben.', id=ctx.guild.id)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name='Muted')
        if name == botchannel or botchannel == "None":
            try:
                await member.remove_roles(mutedrole)
                embed = discord.Embed(title='**Unmute**', colour=get_colour(ctx.message))
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Moderator',
                            value=str(mention), inline=False)
                embed.add_field(name='Spieler',
                            value=str(member.mention), inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + f": Der Moderator {user} hat den Spieler {member} unmuted.", id=ctx.guild.id)
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
                          get_prefix_string(ctx.message) + 'unmute auszuführen..', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' + get_prefix_string(ctx.message) +
                      'unmute im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @unmute.error
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
                      get_prefix_string(ctx.message) + 'unmute zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'unmute <@Spieler>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'unmute eingegeben.', id=ctx.guild.id)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def blacklist(self, ctx, type, *, word):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        path = os.path.join('data', 'blacklist', f'{ctx.guild.id}.json')
        bannedWords = get_blacklist(path)
        if name == botchannel or botchannel == "None":
            if type == "add":
                if word.lower() in bannedWords:
                    embed = discord.Embed(title='**Fehler**', description=f'Das Wort ```{word}```'
                    ' ist bereits auf der Blacklist!', colour=get_colour(ctx.message))
                    embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                    await ctx.send(embed=embed)
                    log(f'{time}: Der Moderator {user} hat versucht das Wort "{word}" zur Blacklist hinzufügen,'
                        ' es war aber schon drauf.', id=ctx.guild.id)
                else:
                    bannedWords.append(word.lower())
                    writejson(type="blacklist", input=bannedWords, path=path)
                    await msg2.delete()
                    embed = discord.Embed(title='**Blacklist**', description=f'Das Wort ```{word}```'
                    ' wurde zur Blacklist hinzugefügt!',colour=get_colour(ctx.message))
                    embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                    await ctx.send(embed=embed)
                    log(f'{time}: Der Moderator {user} hat das Wort "{word}" auf die Blacklist hinzugefügt.'
                        , id=ctx.guild.id)
            elif type == "remove":
                if word.lower() in bannedWords:
                    bannedWords.remove(word.lower())
                    writejson(type="blacklist", input=bannedWords, path=path)
                    await ctx.message.delete()
                    embed = discord.Embed(title='**Blacklist**', description=f'Das Wort ```{word}```'
                    ' wurde von der Blacklist entfernt!',colour=get_colour(ctx.message))
                    embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                    await ctx.send(embed=embed)
                    log(f'{time}: Der Moderator {user} hat das Wort "{word}"von der Blacklist entfernt.'
                        , id=ctx.guild.id)
                else:
                    embed = discord.Embed(title='**Fehler**', description=f'Das Wort ```{word}```'
                    ' befindet sich nicht auf der Blacklist!',colour=get_colour(ctx.message))
                    embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                    await ctx.send(embed=embed)
                    log(f'{time}: Der Moderator {user} hat versucht das Wort "{word}" von der Blacklist zu entfernen,'
                        ' es war aber nicht drauf.', id=ctx.guild.id)
            else:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Du hast ein ungültiges Argument angegeben, Nutzung: ```' +
                                      get_prefix_string(ctx.message) + 'blacklist <add/new>```', inline=False)
                await ctx.send(embed=embed)
                log(f'{time}: Der Moderator {user} hat ein ungültiges Argument beim Befehl' +
                get_prefix_string(ctx.message) + 'blacklist eingegeben.', ctx.guild.id)

    @blacklist.error
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
                      get_prefix_string(ctx.message) + 'blacklist zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```' +
                                  get_prefix_string(ctx.message) + 'blacklist <new/add> <Wort>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'blacklist eingegeben.', id=ctx.guild.id)

########################################################################################################################


def setup(bot):
    bot.add_cog(moderation(bot))
