import datetime

from discord.ext import commands

from cogs.commands.Hilfe.help import on_help_button
from cogs.commands.Tools.rechner import on_calculator_button
from cogs.commands.Unterhaltung.say import on_say_button
from cogs.commands.Unterhaltung.ssp import on_ssp_button
from cogs.core.functions.cache import (
    get_messages_from_cache,
)
from cogs.core.functions.logging import log
from config import (
    MISSING_PERMISSIONS_BUTTON_ERROR,
)


class on_button_click(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, res):
        wait_for_buttons = ["restore-blacklist", "restore-trigger"]
        try:
            user = res.author.name
            if (
                    res.component.id not in wait_for_buttons
                    and res.message.id
                    not in await get_messages_from_cache(authorid=res.author.id)
            ):
                await res.respond(content=MISSING_PERMISSIONS_BUTTON_ERROR)
                await log(
                    f"{datetime.datetime.now()}: Der Nutzer {user} hat versucht mit einem Button zu interagieren, hatte aber nicht die nötigen Berrechtigungen.",
                    res.message.guild.id,
                )
                return
            if "help_" in res.component.id:
                await on_help_button(res)
            elif "say_" in res.component.id:
                await on_say_button(res)
            elif "calc_" in res.component.id:
                await on_calculator_button(res)
            elif "ssp_" in res.component.id:
                await on_ssp_button(res)
        except Exception:
            # traceback.print_exc()
            pass


########################################################################################################################


def setup(bot):
    bot.add_cog(on_button_click(bot))
