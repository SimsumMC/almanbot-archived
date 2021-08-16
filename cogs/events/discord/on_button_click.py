import datetime
import traceback

from discord.ext import commands
from discord_components import Button, ButtonStyle, InteractionType
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.commands.Hilfe.help import get_page
from cogs.core.functions.logging import log


class on_button_click(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, res):
        helpp = [
            "allgemein",
            "informationen",
            "unterhaltung",
            "moderation",
            "administration",
            "übersicht",
            "inhaber",
        ]
        user = res.author.name
        try:
            if res.component.label.lower() in helpp:
                embed = get_page(
                    message=res.message, user=user, page=res.component.label.lower()
                )
                await res.respond(
                    type=7,
                    embed=embed,
                    components=[
                        [
                            Button(style=get_buttoncolour(message=res.message), label="Übersicht", emoji="🔖"),
                            Button(style=get_buttoncolour(message=res.message), label="Allgemein", emoji="🤖"),
                            Button(
                                style=get_buttoncolour(message=res.message), label="Informationen", emoji="📉"
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message), label="Unterhaltung", emoji="🎲"
                            ),
                        ],
                        [
                            Button(
                                style=get_buttoncolour(message=res.message), label="Moderation", emoji="🛡"
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message), label="Administration", emoji="⚙"
                            ),
                            Button(style=get_buttoncolour(message=res.message), label="Inhaber", emoji="🔒"),
                        ],
                    ],
                )
                log(
                    f"{datetime.datetime.now()}: Der Spieler {user} hat mit der Hilfenachricht interagiert und die "
                    f"Seite {res.component.label.lower()} aufgerufen!",
                    res.message.guild.id,
                )
            else:
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f"Error 404: Der Button {res.component.label} ist ungültig!",
                )
        except Exception:
            pass


########################################################################################################################


def setup(bot):
    bot.add_cog(on_button_click(bot))
