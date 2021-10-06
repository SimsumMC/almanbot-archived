import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", usage="<@Nutzer> <opt. Grund>")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        if await botchannel_check(ctx):
            if ctx.author.top_role < member.top_role:
                embed = discord.Embed(
                    title="Fehler",
                    description="Du bist in der Hierarchie unter dem Nutzer den du bannen willst, daher bist du zu dieser Aktion nicht berechtigt!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Moderator {user} hat versucht den Nutzer {member.name + member.discriminator} mit dem"
                    f" Befehl {get_prefix_string(ctx.message)}ban zu bannen, war aber dazu nicht berrechtigt.",
                    ctx.guild.id,
                )
                return
            try:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="**Ban**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(name="Moderator:", value=mention, inline=False)
                embed.add_field(name="Nutzer:", value=str(member), inline=False)
                embed.add_field(name="Grund:", value=reason, inline=False)
                await ctx.send(embed=embed)
                await log(
                    str(time)
                    + ": Der Moderator "
                    + str(user)
                    + "hat den Nutzer "
                    + str(member)
                    + ' erfolgreich für "'
                    + str(reason)
                    + '" gebannt.',
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
                    + "ban auszuführen.",
                    guildid=ctx.guild.id,
                )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(ban(bot))
