import datetime

import discord
from discord.ext import commands

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.functions import (
    is_not_pinned,
)
from cogs.core.functions.logging import log


class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["c"], usage="<Anzahl: Zahl von 1 bis 100>")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        if amount < 101:
            try:
                deleted = await ctx.channel.purge(limit=amount + 1, check=is_not_pinned)
                if amount == 1:
                    nachricht = "Nachricht"
                    wurde = "wurde"
                else:
                    nachricht = "Nachrichten"
                    wurde = "wurden"
                embed = discord.Embed(
                    title="Clear",
                    description=f"Es {wurde} {len(deleted) - 1} {nachricht} gelöscht!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                await ctx.send(embed=embed, delete_after=5)
                await log(
                    str(time)
                    + ": Der Nutzer "
                    + str(user)
                    + " hat "
                    + str(len(deleted) - 1)
                    + " Nachrichten im Kanal #"
                    + str(name)
                    + " mit dem Befehl "
                    + await get_prefix_string(ctx.message)
                    + "clear gelöscht.",
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
                    + "clear auszuführen.",
                    guildid=ctx.guild.id,
                )

        else:
            embed = discord.Embed(
                title="**Fehler**",
                description="Du kannst nicht über 100 Nachrichten  aufeinmal löschen!"
                " Nutze dazu bitte !channelclear .",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed, delete_after=5)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat probiert "
                + str(amount - 1)
                + " Nachrichten im Kanal #"
                + str(name)
                + " mit dem Befehl "
                + await get_prefix_string(ctx.message)
                + "clear zu löschen, hat aber das "
                "Limit von 100 Nachrichten überschritten!",
                guildid=ctx.guild.id,
            )


########################################################################################################################


def setup(bot):
    bot.add_cog(clear(bot))
