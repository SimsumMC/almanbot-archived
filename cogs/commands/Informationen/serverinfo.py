import datetime
import discord
from discord.ext import commands
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class serverinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
                                                             f"`{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}`\n"
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

########################################################################################################################


def setup(bot):
    bot.add_cog(serverinfo(bot))