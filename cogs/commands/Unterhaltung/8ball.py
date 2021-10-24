import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class eightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answers = [
            "Ja",
            "Nein",
            "Vielleicht",
            "Wahrscheinlich",
            "Sieht so aus",
            "Sehr wahrscheinlich",
            "Sehr unwahrscheinlich",
        ]

    @commands.command(
        name="8ball", aliases=["question", "answer", "frage"], usage="<Frage>"
    )
    async def _eightball(self, ctx: commands.Context, *, question):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        answer = random.choice(self.answers)
        embed = discord.Embed(title="8Ball", colour=await get_embedcolour(ctx.message))
        embed.add_field(name="**Deine Frage**", value=str(question), inline=False)
        embed.add_field(name="**Meine Antwort**", value=str(answer) + ".", inline=False)
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "example benutzt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(eightball(bot))
