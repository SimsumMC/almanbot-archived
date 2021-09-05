import datetime

import discord
from discord.ext import commands
from discord_components import Button

from cogs.commands.Hilfe.help import get_page, get_help_buttons
from cogs.commands.Tools.rechner import calculate
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.cache import (
    get_messages_from_cache,
)
from cogs.core.functions.logging import log
from config import (
    CALCULATING_ERROR,
    MISSING_PERMISSIONS_BUTTON_ERROR,
)


class on_button_click(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, res):
        if res.message.id not in get_messages_from_cache(authorid=res.author.id):
            await res.respond(content=MISSING_PERMISSIONS_BUTTON_ERROR)
            return

        user = res.author.name
        try:
            help_buttons = [
                "help_allgemein",
                "help_informationen",
                "help_unterhaltung",
                "help_moderation",
                "help_administration",
                "help_übersicht",
                "help_tools",
                "help_inhaber",
                "help_musik",
            ]
            if res.component.id in help_buttons:
                embed = get_page(message=res.message, page=res.component.id[5:])
                await res.respond(
                    type=7, embed=embed, components=get_help_buttons(res.message)
                )
                log(
                    f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Hilfenachricht interagiert und die "
                    f"Seite {res.component.label.lower()} aufgerufen!",
                    res.message.guild.id,
                )
            elif res.component.id == "say_normal":
                await res.respond(
                    type=7,
                    content=res.message.embeds[0].description,
                    embeds=[],
                    components=[
                        [
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="Normal",
                                emoji="📄",
                                id="say_normal",
                                disabled=True,
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="Embed",
                                emoji="✒",
                                id="say_embed",
                                disabled=False,
                            ),
                        ]
                    ],
                )
                log(
                    f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Say-Nachricht interagiert!",
                    res.message.guild.id,
                )
            elif res.component.id == "say_embed":
                embed = discord.Embed(
                    title="**Say**",
                    description=str(res.message.content),
                    colour=get_embedcolour(res.message),
                )
                embed._footer = get_embed_footer(message=res.message)
                embed._thumbnail = get_embed_thumbnail()
                await res.respond(
                    type=7,
                    embed=embed,
                    content=" ",
                    components=[
                        [
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="Normal",
                                emoji="📄",
                                id="say_normal",
                                disabled=False,
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="Embed",
                                emoji="✒",
                                id="say_embed",
                                disabled=True,
                            ),
                        ]
                    ],
                )
                log(
                    f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Say-Nachricht interagiert!",
                    res.message.guild.id,
                )
            elif "calc_" in res.component.id:
                description = str(res.message.embeds[0].description)[:-3][3:]
                if description == CALCULATING_ERROR + "|":
                    description = "|"
                elif res.component.label == "x" and description[-2] == "x":
                    pass
                elif res.component.label == "Exit":
                    await res.respond(
                        type=7,
                        content="Rechner geschlossen!",
                        components=[
                            [
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="1",
                                    id="calc_1",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="2",
                                    id="calc_2",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="3",
                                    id="calc_3",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="x",
                                    id="calc_x",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="Exit",
                                    id="calc_exit",
                                    disabled=True,
                                ),
                            ],
                            [
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="4",
                                    id="calc_4",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="5",
                                    id="calc_5",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="6",
                                    id="calc_6",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="÷",
                                    id="calc_division",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="⌫",
                                    id="calc_delete",
                                    disabled=True,
                                ),
                            ],
                            [
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="7",
                                    id="calc_7",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="8",
                                    id="calc_8",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="9",
                                    id="calc_9",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="+",
                                    id="calc_addition",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="Clear",
                                    id="calc_clear",
                                    disabled=True,
                                ),
                            ],
                            [
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="00",
                                    id="calc_00",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="0",
                                    id="calc_0",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label=".",
                                    id="calc_comma",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="-",
                                    id="calc_subtraction",
                                    disabled=True,
                                ),
                                Button(
                                    style=get_buttoncolour(message=res.message),
                                    label="=",
                                    id="calc_equal",
                                    disabled=True,
                                ),
                            ],
                        ],
                    )
                elif res.component.label == "⌫":
                    description = description[:-2] + "|"
                elif res.component.label == "Clear":
                    description = "|"
                elif res.component.label == "=":
                    description = str(calculate(description[:-1])) + "|"
                # elif res.coomponent.label == "x" and description[-2] == "x|":
                # pass
                else:
                    description = description[:-1] + res.component.label + "|"
                description = "```" + description + "```"
                embed = discord.Embed(
                    title=f"**{res.author.name}'s Rechner**",
                    description=description,
                    colour=get_embedcolour(res.message),
                )
                embed._footer = get_embed_footer(message=res.message)
                await res.respond(
                    type=7,
                    embed=embed,
                    components=[
                        [
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="1",
                                id="calc_1",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="2",
                                id="calc_2",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="3",
                                id="calc_3",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="x",
                                id="calc_x",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="Exit",
                                id="calc_exit",
                            ),
                        ],
                        [
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="4",
                                id="calc_4",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="5",
                                id="calc_5",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="6",
                                id="calc_6",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="÷",
                                id="calc_division",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="⌫",
                                id="calc_delete",
                            ),
                        ],
                        [
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="7",
                                id="calc_7",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="8",
                                id="calc_8",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="9",
                                id="calc_9",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="+",
                                id="calc_addition",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="Clear",
                                id="calc_clear",
                            ),
                        ],
                        [
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="00",
                                id="calc_00",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="0",
                                id="calc_0",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label=".",
                                id="calc_comma",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="-",
                                id="calc_subtraction",
                            ),
                            Button(
                                style=get_buttoncolour(message=res.message),
                                label="=",
                                id="calc_equal",
                            ),
                        ],
                    ],
                )
            else:
                await res.respond(
                    content=f"Error 404: Diesen Button {res.component.label} kenne ich leider nicht!"
                )
        except Exception:
            # traceback.print_exc()
            pass


########################################################################################################################


def setup(bot):
    bot.add_cog(on_button_click(bot))
