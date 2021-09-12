import datetime

from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button
from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.cache import save_message_to_cache
from cogs.core.functions.logging import log
from main import blacklist_check


class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<Text>")
    async def say(self, ctx, *, text: commands.clean_content):
        time = datetime.datetime.now()
        msg2 = ctx.message
        user = ctx.author.name
        if botchannel_check(ctx):
            if await blacklist_check(self, ctx.message):
                return
            msg = await ctx.send(
                content=str(text),
                components=[
                    [
                        Button(
                            style=get_buttoncolour(message=ctx.message),
                            label="Normal",
                            emoji="📄",
                            id="say_normal",
                            disabled=True,
                        ),
                        Button(
                            style=get_buttoncolour(message=ctx.message),
                            label="Embed",
                            emoji="✒",
                            id="say_embed",
                        ),
                    ]
                ],
            )
            await save_message_to_cache(message=msg, author=msg2.author)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "ssp benutzt!",
                guildid=ctx.guild.id,
            )

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(say(bot))
