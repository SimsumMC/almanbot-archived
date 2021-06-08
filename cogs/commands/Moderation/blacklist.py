import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour, get_blacklist \
    , writejson


class blacklist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
                                                                          ' ist bereits auf der Blacklist!',
                                          colour=get_colour(ctx.message))
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
                                                                             ' wurde zur Blacklist hinzugefügt!',
                                          colour=get_colour(ctx.message))
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
                                                                             ' wurde von der Blacklist entfernt!',
                                          colour=get_colour(ctx.message))
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
                                                                          ' befindet sich nicht auf der Blacklist!',
                                          colour=get_colour(ctx.message))
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
                            value='Dir fehlt folgende Berrechtigung um den Befehl auszuführen: '
                                  '```ban_members```',
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
    bot.add_cog(blacklist(bot))