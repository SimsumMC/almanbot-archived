import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.functions.logging import log
from config import ICON_URL, FOOTER, WRONG_CHANNEL_ERROR


class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", aliases=["m"], usage="<@Nutzer> <opt. Grund>")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Muted")
        if botchannel_check(ctx):
            try:
                if not mutedrole:
                    mutedrole = await guild.create_role(name="Muted")
                    for channel in guild.channels:
                        await channel.set_permissions(
                            mutedrole,
                            speak=False,
                            send_messages=False,
                            read_message_history=True,
                            read_messages=True,
                        )
                await member.add_roles(mutedrole, reason=reason)
                embed = discord.Embed(
                    title="**Mute**", colour=get_embedcolour(ctx.message)
                )
                embed.set_footer(
                    text=FOOTER[0]
                    + str(user)
                    + FOOTER[1]
                    + str(get_author())
                    + FOOTER[2]
                    + str(get_prefix_string(ctx.message)),
                    icon_url=ICON_URL,
                )
                embed.add_field(name="Moderator", value=str(mention), inline=False)
                embed.add_field(name="Nutzer", value=str(member.mention), inline=False)
                embed.add_field(name="Grund", value=str(reason), inline=False)
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + f": Der Moderator {user} hat den Nutzer {member} für {reason} gemuted.",
                    guildid=ctx.guild.id,
                )
            except Exception:
                embed = discord.Embed(
                    title="**Fehler**", colour=get_embedcolour(ctx.message)
                )
                embed.set_footer(
                    text="for "
                    + str(user)
                    + " | by "
                    + str(get_author())
                    + " | Prefix "
                    + get_prefix_string(message=ctx.message),
                    icon_url="https://media.discordapp.net/attachments/645276319311200286/803322491480178739"
                    "/winging-easy.png?width=676&height=676",
                )
                embed.add_field(
                    name="‎",
                    value="Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                log(
                    text=str(time)
                    + ": Der Bot hatte nicht die nötigen Berrechtigungen um "
                    + get_prefix_string(ctx.message)
                    + "mute auszuführen..",
                    guildid=ctx.guild.id,
                )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(mute(bot))
