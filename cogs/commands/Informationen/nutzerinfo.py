import datetime
import discord
from discord.ext import commands
from cogs.core.functions.functions import log, get_author, get_prefix_string, get_botc, get_colour, whoisr


class nutzerinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["userinfo", "whois", "userstats", "nutzerstats"])
    async def nutzerinfo(self, ctx, member: discord.Member = None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        botchannel = get_botc(message=ctx.message)
        if name == botchannel or botchannel == 'None':
            if member is None:
                member = ctx.author
            roles = [role for role in member.roles]

            embed = discord.Embed(title=f"**Nutzerinfo für {member}**", colour=get_colour(ctx.message))
            embed.set_footer(text='for ' + str(user) + ' | by ' + str(get_author()) + ' | Prefix ' + get_prefix_string(
                message=ctx.message), icon_url='https://media.discordapp.net/attachments/645276319311200286'
                                               '/803322491480178739/winging-easy.png?width=676&height=676')
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="**Nutzername:**", value=member.display_name, inline=True)
            embed.add_field(name="**ID:**", value=member.id, inline=True)

            embed.add_field(name="**Tag:**", value=member.discriminator, inline=True)
            embed.add_field(name="Aktuelle Aktivität:",
                            value=f" {member.activity.name}" if member.activity is not None else "Keine",
                            inline=True)
            embed.add_field(name="**Erstellt am:**", value=member.created_at.strftime("%d.%m.%y um %H:%M"),
                            inline=True)
            embed.add_field(name="**Beigetreten am:**", value=member.joined_at.strftime("%d.%m.%y um %H:%M"),
                            inline=True)
            embed.add_field(name=f"**Rollen ({len(roles) - 1}):**", value=" **|** "
                            .join([role.mention for role in roles if not role.is_default()]),
                            inline=True)
            embed.add_field(name="**Höchste Rolle:**", value=member.top_role.mention, inline=True)
            embed.add_field(name="**Bot?:**", value=str(whoisr(member=member)), inline=True)
            await ctx.send(embed=embed)
            log(str(time) + ': Der Spieler ' + str(user) + ' hat den Befehl  ' +
                get_prefix_string(ctx.message) + 'nutzerinfo benutzt!', ctx.guild.id)
        else:
            log(input=str(time) + ': Der Spieler ' + str(
                user) + ' hat probiert den Befehl ' +
                      get_prefix_string(ctx.message) + 'nutzerinfo im Channel #' + str(botchannel) + ' zu benutzen!',
                id=ctx.guild.id)
            await ctx.send(str(mention) + ', dieser Befehl kann nur im Kanal #{} genutzt werden.'.format(botchannel),
                           delete_after=3)
            await msg2.delete()

########################################################################################################################


def setup(bot):
    bot.add_cog(nutzerinfo(bot))