import datetime
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class invite(commands.Cog):

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
            embed = discord.Embed(title='**Invite**', color=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + str(
                get_prefix_string(ctx.message)),
                             icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                      '/winging-easy.png?width=676&height=676')
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external"
                                    "/wgxUpO7jSZw0GoWUvh7Y2bTQXUjSvD3QbiMmKgK9wtg/%3Fwidth%3D676%26height%3D676/https"
                                    "/media.discordapp.net/attachments/645276319311200286/803322491480178739/winging"
                                    "-easy.png")
            embed.add_field(name="**Link**", value="https://discord.com/oauth2/authorize?client_id=802922765782089738"
                                                   "&scope=bot&permissions=2620914775")
            await ctx.send(embed=embed,
                           components=[[
                               Button(style=ButtonStyle.URL, label="Klicke hier um mich zu einem Server hinzuzufügen!",
                                      url="https://discord.com/oauth2/authorize?"
                                          "client_id=802922765782089738&scope=bot&permissions=2620914775"),
                               Button(style=ButtonStyle.URL, label="Discord",
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

########################################################################################################################


def setup(bot):
    bot.add_cog(invite(bot))