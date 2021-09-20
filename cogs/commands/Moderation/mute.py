import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log


class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", aliases=["m"], usage="<@Nutzer> <opt. Grund>")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Muted")
        if await botchannel_check(ctx):
            if ctx.author.top_role < member.top_role:
                embed = discord.Embed(
                    title="Fehler",
                    description="Du bist in der Hierarchie unter dem Nutzer den du muten willst, daher bist du zu dieser Aktion nicht berechtigt!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Moderator {user} hat versucht den Nutzer {member.name + member.discriminator} mit dem"
                    f" Befehl {await get_prefix_string(ctx.message)}mute zu muten, war aber dazu nicht berrechtigt.",
                    ctx.guild.id,
                )
                return
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
                    title="**Mute**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(name="Moderator", value=str(mention), inline=False)
                embed.add_field(name="Nutzer", value=str(member.mention), inline=False)
                embed.add_field(name="Grund", value=str(reason), inline=False)
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + f": Der Moderator {user} hat den Nutzer {member} für {reason} gemuted.",
                    guildid=ctx.guild.id,
                )
            except Exception:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Ich habe nicht die nötigen Berrechtigungen um diesen Befehl auszuführen!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Bot hatte nicht die nötigen Berrechtigungen um "
                    + await get_prefix_string(ctx.message)
                    + "mute auszuführen..",
                    guildid=ctx.guild.id,
                )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(mute(bot))
