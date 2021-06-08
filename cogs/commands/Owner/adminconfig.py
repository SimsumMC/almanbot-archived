import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from cogs.core.functions.functions import get_author, get_prefix_string, get_botc, get_colour, redditnsfwcheck \
    , get_memes, get_checkedmemes, writejson, readjson, colour_check, get_colour_code, log


class adminconfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def adminconfig(self, ctx, guildid, subcommand, arg):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg2 = ctx.message
        name = ctx.channel.name
        path = os.path.join('data', 'configs', f'{guildid}.json')
        channel = get_botc(message=ctx.message)
        existing = ['prefix', 'botchannel', 'memechannel', 'memesource', 'colour', 'hilfe']
        if name == channel or channel == "None":
            if subcommand in existing:
                if subcommand == "colour":
                    if colour_check(arg) is True:
                        writejson(type=subcommand, input=get_colour_code(str(arg)), path=path)
                        embed = discord.Embed(title='**Admin Config**', description='Das Modul ```' + str(subcommand)
                                                                              + '``` wurde erfolgreich zu ```' + str(
                            arg) + '``` geändert!'
                                              , colour=get_colour(ctx.message))
                        embed.set_footer(
                            text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                                message=ctx.message),
                            icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                     '/winging-easy.png?width=676&height=676')
                        await ctx.send(embed=embed)
                        return
                    else:
                        embed = discord.Embed(title='**Fehler**', description='Das Modul ```' + str(subcommand)
                                                                              + '``` kann nicht zu ```' + str(
                            arg) + '``` geändert werden.'
                                              , colour=get_colour(ctx.message))
                        embed.set_footer(
                            text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                                message=ctx.message),
                            icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                     '/winging-easy.png?width=676&height=676')
                        await ctx.send(embed=embed)
                        return

                elif subcommand == "memesource":
                    path2 = os.path.join('data', 'verifiedmemes', 'memes.json')
                    if arg == "default":
                        arg = "memes"
                    if arg != get_memes(guildid) and get_checkedmemes(arg) is False:
                        if arg in readjson("failed", path2) or redditnsfwcheck(arg):
                            embed = discord.Embed(title="**Fehler**",
                                                  description=f"Der angegebene Reddit **{arg}** enthält nicht "
                                                              "zulässigen Inhalt.",
                                                  color=get_colour(ctx.message))
                            embed.set_thumbnail(
                                url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739/winging-easy'
                                    '.png?width=676&height=676')
                            embed.set_footer(
                                text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                                    get_prefix_string(message=ctx.message)),
                                icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                         '/803322491480178739/winging-easy.png?width=676&height=676')
                            await ctx.send(embed=embed)
                            return
                writejson(type=subcommand, input=arg, path=path)
                embed = discord.Embed(title='**Admin Config**', colour=get_colour(ctx.message))
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
            else:
                embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
                embed.set_footer(
                    text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                        message=ctx.message),
                    icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                             '/winging-easy.png?width=676&height=676')
                embed.add_field(name='‎',
                                value='Das Modul **' + str(subcommand) + '** existiert nicht!',
                                inline=False)
                await ctx.send(embed=embed)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'papier im Channel #' + str(channel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                           delete_after=3)
            await msg2.delete()


    @adminconfig.error
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
                                  get_prefix_string(ctx.message) + 'config <Guild ID> <Modul> <Wert>```',
                            inline=False)
            await ctx.send(embed=embed)


########################################################################################################################


def setup(bot):
    bot.add_cog(adminconfig(bot))