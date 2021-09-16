import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer
from cogs.core.functions.logging import log


class serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        if await botchannel_check(ctx):
            embed = discord.Embed(
                title=f"**Serverinfo für {ctx.guild.name}**",
                colour=await get_embedcolour(ctx.message),
            )
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="**Name:**", value=ctx.guild.name, inline=True)
            embed.add_field(name="**ID:**", value=ctx.guild.id, inline=True)
            embed.add_field(name="**Region:**", value=ctx.guild.region, inline=True)
            embed.add_field(
                name="**Erstellt am:**",
                value=ctx.guild.created_at.strftime("%d.%m.%y um %H:%M"),
                inline=True,
            )
            embed.add_field(
                name="**Besitzer:**", value=ctx.guild.owner.mention, inline=True
            )
            embed.add_field(
                name="**Nutzerzahlen:**",
                value=f"Gesamt: `{ctx.guild.member_count}`\n"
                "Nutzer: "
                f"`{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}`\n"
                "Bots: "
                f"`{len(list(filter(lambda m: m.bot, ctx.guild.members)))}`\n",
                inline=True,
            )
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl  "
                + await get_prefix_string(ctx.message)
                + "serverinfo benutzt!",
                ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(serverinfo(bot))
