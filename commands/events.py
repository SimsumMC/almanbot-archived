import datetime
import json
import os
from shutil import copyfile
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from commands.functions import get_prefix, get_botc, get_author, get_prefix_string, get_colour
from commands.functions import log


class events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg = ctx.message.content
        msg2 = ctx.message
        name = ctx.channel.name
        channel = get_botc(message=ctx.message)
        if isinstance(error, CommandNotFound):
            if name == channel or channel == "None":
                embed = discord.Embed(title="Fehler", description='Der Befehl "' + str(msg) + '" existiert nicht!',
                                      color=get_colour(ctx.message))
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' +
                                 get_prefix_string(message=ctx.message),
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                          '/803322491480178739'
                                          '/winging-easy.png?width=676&height=676')
                await ctx.send(embed=embed)
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat probiert den ungültigen Befehl "' + str(
                    msg) + '" zu nutzen!', id=ctx.guild.id)
            else:
                log(input=str(time) + ': Der Spieler ' + str(user) + ' hat probiert den ungültigen Befehl "' + str(
                    msg) + '" zu nutzen!', id=ctx.guild.id)
                await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(channel),
                               delete_after=3)
                await msg2.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        path = os.path.join('data', 'configs', f'{guild.id}.json')
        pathcheck = os.path.join('data', 'configs', 'deleted', f'{guild.id}.json')
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
        else:
            with open(path, 'w') as f:
                data = {"prefix": "!",
                        "botchannel": "None",
                        "memechannel": "None",
                        "memesource":"memes",
                        "colour": 13372193}
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        path = os.path.join('data', 'configs', f'{guild.id}.json')
        path2 = os.path.join('data', 'logs', f'{guild.id}.txt')
        dest = os.path.join('data', 'configs','deleted', f'{guild.id}.json')
        copyfile(path, dest)
        os.remove(path)
        os.remove(path2)


########################################################################################################################


def setup(bot):
    bot.add_cog(events(bot))
