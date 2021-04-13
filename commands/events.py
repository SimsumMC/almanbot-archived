import datetime
import json
import os
from shutil import copyfile
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from commands.functions import get_prefix, get_botc, get_author
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
                embed = discord.Embed(colour=13372193)
                embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author) + ' | Prefix (get_prefix comming)',
                                 icon_url='https://media.discordapp.net/attachments/645276319311200286/803322491480178739'
                                          '/winging-easy.png?width=676&height=676')
                embed.add_field(name='Fehler', value='Der Befehl "' + str(msg) + '" existiert nicht!',
                                inline=False)
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
        path = "data\\configs\\" + str(guild.id) + ".json"
        pathcheck = "data\\configs\\deleted\\" + str(guild.id) + ".json"
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
        else:
            with open(path, 'w') as f:
                data = {"prefix": "!",
                        "botchannel": "None",
                        "memechannel": "None"}
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        path = "data\\configs\\" + str(guild.id) + ".json"
        path2 = 'data\\logs\\' + str(guild.id) + '.txt'
        dest = "data\\configs\\deleted\\" + str(guild.id) + ".json"
        copyfile(path, dest)
        os.remove(path)
        os.remove(path2)
    ##########################################


def setup(bot):
    bot.add_cog(events(bot))
