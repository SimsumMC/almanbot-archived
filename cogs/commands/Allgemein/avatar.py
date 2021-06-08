import datetime

import discord
from discord.ext import commands
from discord.ext.commands import BadArgument

from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour


class avatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self,  ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            if member is None:
                member = ctx.author
            embed = discord.Embed(title=f"**Avatar von {member.display_name}**", colour=get_colour(ctx.message))
            embed.set_image(url=member.avatar_url)
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' +
                                  get_prefix_string(message=ctx.message), icon_url='https://media.discordapp.net/'
                                                                                   'attachments/645276319311200286'
                                                                                   '/803322491480178739/winging-easy.png?width=676&height=676')
            await ctx.send(embed=embed)
            log(f'{time}: Der Spieler {user} hat den Befehl {get_prefix_string(ctx.message)}'
                'avatar benutzt!', id=ctx.guild.id)
        else:
            log(input=f'{time}: Der Spieler {user} hat probiert den Befehl {get_prefix_string(ctx.message)}'
                      f'avatar im Channel #{name} zu benutzen!', id=ctx.guild.id)
            await ctx.send(f'{mention}, dieser Befehl kann nur im Kanal #{botchannel} genutzt werden.',
                           delete_after=3)
            await msg2.delete()

    @avatar.error
    async def handle_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        if isinstance(error, BadArgument):
            embed = discord.Embed(title='**Fehler**', colour=get_colour(ctx.message))
            embed.set_footer(
                text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                    message=ctx.message),
                icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                         '/winging-easy.png?width=676&height=676')
            embed.add_field(name='‎',
                            value='Du musst den Spieler erwähnen, also z.B. @Spieler#1234 !',
                            inline=False)
            await ctx.send(embed=embed)
            log(input=str(time) + ': Der Spieler ' + str(user) + ' hat ein ungültiges Argument bei ' +
                      get_prefix_string(ctx.message) + 'avatar angegeben.', id=ctx.guild.id)


########################################################################################################################


def setup(bot):
    bot.add_cog(avatar(bot))
