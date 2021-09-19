import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log


class unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<Nutzer#1234>")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        if await botchannel_check(ctx):
            if "#" not in member:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Du musst den Nutzer mit dem Tag angeben, also z.B. Nutzer#1234 !",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Nutzer "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + await get_prefix_string(ctx.message)
                    + "unban angegeben.",
                    guildid=ctx.guild.id,
                )
                return
            elif "<@" in member and ">" in member:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Du musst den Nutzer mit dem Tag angeben, also z.B. Nutzer#1234 !",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await log(
                    text=str(time)
                    + ": Der Nutzer "
                    + str(user)
                    + " hat ein ungültiges Argument bei "
                    + await get_prefix_string(ctx.message)
                    + "unban angegeben.",
                    guildid=ctx.guild.id,
                )
                return
            banned_users = await ctx.guild.bans()
            member_name, member_disc = member.split("#")
            for ban_entry in banned_users:
                user2 = ban_entry.user
                if (user2.name, user2.discriminator) == (member_name, member_disc):
                    try:
                        await ctx.guild.unban(user2)
                        embed = discord.Embed(
                            title="**Unban**", colour=await get_embedcolour(ctx.message)
                        )
                        embed._footer = await get_embed_footer(ctx)
                        embed._thumbnail = await get_embed_thumbnail()
                        embed.add_field(name="Moderator:", value=mention, inline=False)
                        embed.add_field(name="Nutzer:", value=str(member), inline=False)
                        await ctx.send(embed=embed)
                        await log(
                            str(time)
                            + ": Der Moderator "
                            + str(user)
                            + "hat den Nutzer "
                            + str(member)
                            + " erfolgreich entbannt.",
                            guildid=ctx.guild.id,
                        )
                        return
                    except Exception:
                        embed = discord.Embed(
                            title="**Fehler**",
                            colour=await get_embedcolour(ctx.message),
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
                            + "unban auszuführen..",
                            guildid=ctx.guild.id,
                        )
                        return
            else:
                embed = discord.Embed(
                    title="**Fehler**",
                    description="Der Nutzer "
                    + str(member)
                    + " ist nicht gebannt und kann daher "
                    "auch nicht entbannt werden.",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed)
                await log(
                    str(time)
                    + ": Der Moderator "
                    + str(user)
                    + "hat versucht den  ungültigen Nutzer "
                    + str(member)
                    + " zu entbannen.",
                    guildid=ctx.guild.id,
                )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(unban(bot))
