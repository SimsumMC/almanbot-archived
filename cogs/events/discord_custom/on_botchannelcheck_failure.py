import datetime

import discord
from discord.ext import commands
from cogs.core.config.config_botchannel import get_botchannel_obj_list
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.logging import log
from cogs.core.functions.ctx_utils import get_commandname
from config import WRONG_CHANNEL_ERROR, ICON_URL, WRONG_CHANNEL_ERROR_DELETE_AFTER


class on_botchannelcheck_failure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_botchannelcheck_failure(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        msg2 = ctx.message
        name = get_commandname(ctx)
        log(
            text=f"{time}: Der Nutzer {user} hat probiert den Befehl {get_prefix_string(ctx.message)}"
                 f"join im Channel #{name} zu benutzen!",
            guildid=ctx.guild.id,
        )
        embed = discord.Embed(
            title="**Fehler**",
            description=WRONG_CHANNEL_ERROR,
            colour=get_embedcolour(message=ctx.message),
        )
        embed.set_footer(
            text=get_embed_footer_text(ctx),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name="‎",
            value=get_botchannel_obj_list(ctx),
            inline=False,
        )
        await ctx.send(embed=embed, delete_after=WRONG_CHANNEL_ERROR_DELETE_AFTER)
        await msg2.delete()

########################################################################################################################


def setup(bot):
    bot.add_cog(on_botchannelcheck_failure(bot))
