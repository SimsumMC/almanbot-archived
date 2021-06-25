import datetime
import discord
import whois
import socket
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, BadArgument

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour, whoisr


class lookup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lookup(self, ctx, domain: str):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            if "http" in domain:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Du musst eine Domain ohne http/-s angeben, z.B. ```example.org```',
                                inline=True)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat ein ungültiges Argument bei ' +
                          get_prefix_string(ctx.message) + 'lookup angegeben.', id=ctx.guild.id)
                return
            w = whois.whois(domain)
            if w.domain_name is None:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                        text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                            message=ctx.message),
                        icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                 '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                    value='Du musst eine existierende Domain angeben, z.B. ```example.org```',
                                    inline=True)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat ein ungültiges Argument bei ' +
                              get_prefix_string(ctx.message) + 'lookup angegeben.', id=ctx.guild.id)
                return
            embed = discord.Embed(title=f'**Informationen zur Domain {domain}**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy.png'
                    '?width=676&height=676')
            embed.add_field(name='**Domain:**', value=w.domain_name, inline=True)
            embed.add_field(name='**Registrar:**', value=w.registrar, inline=True)
            embed.add_field(name='**IP:**', value=f"{socket.gethostbyname(domain)}", inline=True)
            embed.add_field(name='**Standort:**', value=f"{w.state} / {w.country}", inline=True)
            embed.add_field(name='**Buchungsdatum:**', value=w.creation_date, inline=True)
            embed.add_field(name='**Auslaufdatum:**', value=w.expiration_date, inline=True)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' + get_prefix_string(ctx.message) +
                'meme benutzt!', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'lookup im Channel #' + str(name) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @lookup.error
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
                                  get_prefix_string(ctx.message) + 'lookup <Domain>```'
                            '`Hinweis: Bitte ohne http/-s angeben, also z.B. communitybot.visitlink.de`',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'lookup eingegeben.', id=ctx.guild.id)
        if isinstance(error, BadArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(
                text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                    message=ctx.message),
                icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                         '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du musst eine richtige Domain angeben, z.B. ```communitybot.visitlink.de```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(user) + ' hat ein ungültiges Argument bei ' +
                      get_prefix_string(ctx.message) + 'lookup angegeben.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(lookup(bot))