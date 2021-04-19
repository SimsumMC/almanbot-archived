import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument

from commands.functions import get_botc, log, get_author, get_prefix_string, writejson
from main import client


class administrator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def botlog(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg = ctx.message.content
        msg2 = ctx.message
        name = ctx.channel.name
        path = 'data\\logs\\' + str(ctx.guild.id) + '.txt'
        channel = get_botc(message=ctx.message)
        if name == channel or channel == "None":
            if os.path.isfile(path):
                await ctx.send(file=discord.File(path))
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat sich den Log mit der ID "' + str(
                    ctx.guild.id) + '" ausgeben lassen!', id=ctx.guild.id)
            else:
                embed = discord.Embed(title='Fehler', colour=13372193)
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster '
                                      'Befehl ist!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(
                    user) + ' hat sich probiert den noch nicht existierenden Log mit der ID "' + str(
                    ctx.guild.id) + '" ausgeben zu lassen!', id=ctx.guild.id)

        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl !serverlog im Channel #' + str(channel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()

    @botlog.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title='Fehler', colour=13372193)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um !botlog zu nutzen.', id=ctx.guild.id)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, subcommand, arg):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg = ctx.message.content
        msg2 = ctx.message
        name = ctx.channel.name
        path = "data\\configs\\" + str(ctx.guild.id) + ".json"
        channel = get_botc(message=ctx.message)
        existing = ['prefix', 'botchannel', 'memechannel']
        if name == channel or channel == "None":
            if subcommand in existing:
                writejson(type=subcommand, input=arg, path=path)
                embed = discord.Embed(title='Config', colour=13372193)
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Das Modul ```' + str(subcommand) + '``` wurde erfolgreich zu ```' + str(
                                    arg) + '``` geändert!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !Config benutzt und damit das '
                                                                     'Modul ' + str(subcommand) + ' zu' + str(
                    arg) + ' erfolgreich geändert', id=ctx.guild.id)
            else:
                embed = discord.Embed(title='Fehler', colour=13372193)
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Das Modul ' + str(subcommand) + 'existiert nicht!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(
                    user) + ' hat probiert den Befehl !Config zu benutzen und damit das '
                            'Modul ' + str(subcommand) + ' zu' + str(arg) + ' zu ändern.', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl !serverlog im Channel #' + str(channel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()

    @config.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title='Fehler', colour=13372193)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um !config zu nutzen.', id=ctx.guild.id)
        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title='Fehler', colour=13372193)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht alle erforderlichen Argumente angegeben, Nutzung: ```!config <Modul> '
                                  '<Wert>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl !config eingegeben.', id=ctx.guild.id)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channelclear(self, ctx):
        channelid = ctx.channel.id
        channel1 = client.get_channel(channelid)
        time = datetime.datetime.now()
        user = ctx.author.name
        await channel1.clone()
        await channel1.delete()
        log(input=str(time) + ': Der Spieler ' + str(user) + ' hat den Chat "#' + str(channel1) + '" gecleart.',
            id=ctx.guild.id)

    @config.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title='Fehler', colour=13372193)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du hast nicht die nötigen Berrechtigungen um diesen Befehl zu nutzen!',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hatte nicht die nötigen Berrechtigungen um !config zu nutzen.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(administrator(bot))
