import datetime

from discord.ext import commands

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
    async def on_button_click(self, interaction):
        from cogs.commands.Allgemein.help import on_help_button
        from cogs.commands.Tools.giveaways import on_giveaway_button
        from cogs.commands.Tools.rechner import on_calculator_button
        from cogs.commands.Unterhaltung.say import on_say_button
        from cogs.commands.Unterhaltung.ssp import on_ssp_button

        bypass_buttons = [
            "restore-blacklist",
            "restore-trigger",
            "giveaway_preview",
            "giveaway_start",
            "giveaway_cancel",
            "giveaway_join",
            "todo_add_undo",
            "todo_clear_undo",
        ]
        try:
            user = interaction.author.name
            if (
                interaction.component.id not in bypass_buttons
                and interaction.message.id
                not in await get_messages_from_cache(authorid=interaction.author.id)
            ):
                await interaction.respond(content=MISSING_PERMISSIONS_BUTTON_ERROR)
                await log(
                    f"{datetime.datetime.now()}: Der Nutzer {user} hat versucht mit einem Button zu interagieren, hatte dazu aber nicht die nötigen Berrechtigungen.",
                    interaction.message.guild.id,
                )
                return
            if "help_" in interaction.component.id:
                await on_help_button(interaction)
            elif "say_" in interaction.component.id:
                await on_say_button(interaction)
            elif "calc_" in interaction.component.id:
                await on_calculator_button(interaction)
            elif "ssp_" in interaction.component.id:
                await on_ssp_button(interaction)
            elif "giveaway" in interaction.component.id:
                await on_giveaway_button(interaction)
        except Exception:
            # traceback.print_exc()
            pass


########################################################################################################################


def setup(bot):
    bot.add_cog(on_button_click(bot))
