import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, BadArgument
from discord_components import Button, ButtonStyle
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class loeschdich(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["löschdich", "delteyou", "deletuser", "löschenutzer"])
    async def loeschdich(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(ctx.message)
        if name == botchannel or botchannel == "None":
            if reason is None:
                reason = "Kein Grund angegeben, den kennst du bestimmt selber!"
            link = f"https://löschdich.de/{member.display_name}"
            link.replace(" ", "-")
            embed = discord.Embed(title=f'**Lösch dich {member.display_name}!**', colour=get_colour(ctx.message))
            embed.set_thumbnail(
                url='https://images-ext-1.discordapp.net/external/wgxUpO7jSZw0GoWUvh7Y2bTQXUjSvD3QbiMmKgK9wtg'
                    '/%3Fwidth%3D676%26height%3D676/https/media.discordapp.net/attachments/645276319311200286'
                    '/803322491480178739/winging-easy.png')
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.add_field(name='**Link**', value=str(link), inline=False)
            embed.add_field(name='**Grund**', value=str(reason), inline=False)
            await ctx.send(content=f"{member.mention}, bitte lösch dich einfach aus dem Internet. Klicke "
                                   f"dazu einfach unten auf den Knopf für mehr Informationen! ", embed=embed,
                           components=[
                               Button(style=ButtonStyle.URL, label="Lösch dich Jetzt!", url=link, emoji="🗑")
                           ])
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl ' +
                get_prefix_string(ctx.message) + 'löschdich benutzt!', id=ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'löschdich im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

    @loeschdich.error
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
                                  get_prefix_string(ctx.message) + 'löschdich <@Spieler> <opt. Grund>```',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat nicht alle erforderlichen Argumente beim Befehl ' +
                      get_prefix_string(ctx.message) + 'löschdich eingegeben.', id=ctx.guild.id)
        if isinstance(error, BadArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(
                text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                    message=ctx.message),
                icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                         '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du musst den Spieler mit dem Tag angeben, also z.B. Spieler#1234 !',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(user) + ' hat ein ungültiges Argument bei ' +
                      get_prefix_string(ctx.message) + 'löschdich angegeben.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(loeschdich(bot))
