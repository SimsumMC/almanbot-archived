import datetime
import os
import discord
from discord.ext import commands

from commands.functions import get_botc, log, get_author, get_prefix_string, writejson


class administrator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverlog(self, ctx):
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
                embed = discord.Embed(colour=13372193)
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Fehler', value='Der Befehl "' + str(msg) + '" existiert nicht!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat sich den Log mit der ID "' + str(
                    ctx.guild.id) + '" ausgeben lassen!', id=ctx.guild.id)
                await ctx.send(file=discord.File(path))
            else:
                embed = discord.Embed(colour=13372193)
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Fehler',
                                value='Es existiert noch kein Log deines Servers, da dass hier anscheinend dein erster '
                                      'Befehl ist!',
                                inline=False)
                await ctx.send(embed=embed)

        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl !serverlog im Channel #' + str(channel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()

    @commands.command()
    async def config(self, ctx, subcommand=None, arg=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg = ctx.message.content
        msg2 = ctx.message
        name = ctx.channel.name
        path = "data\\configs\\" + str(ctx.guild.id) + ".json"
        channel = get_botc(message=ctx.message)
        existing = ['prefix', 'botchannel']
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
                                value='Das Modul ```' + str(subcommand) + '``` wurde erfolgreich zu ```' + str(arg) + '``` geändert!',
                                inline=False)
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl !Config benutzt und damit das '
                    'Modul ' + str(subcommand) + ' zu' + str(arg) + ' erfolgreich geändert', id=ctx.guild.id)
            else:
                embed = discord.Embed(colour=13372193)
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Fehler',
                                value='Der Sub-Befehl ' + str(subcommand) +'existiert nicht!',
                                inline=False)
                await ctx.send(embed=embed)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl !serverlog im Channel #' + str(channel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()


def setup(bot):
    bot.add_cog(administrator(bot))
