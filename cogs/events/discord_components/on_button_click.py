import datetime
import traceback

import discord
from discord.ext import commands
from discord_components import Button

from cogs.commands.Hilfe.help import get_page, get_help_buttons
from cogs.commands.Tools.rechner import calculate, get_calculator_buttons
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
        user = res.author.name
        if res.message.id not in await get_messages_from_cache(authorid=res.author.id):
            await res.respond(content=MISSING_PERMISSIONS_BUTTON_ERROR)
            await log(
                f"{datetime.datetime.now()}: Der Nutzer {user} hat versucht mit einem Button zu interagieren, hatte aber nicht die nötigen Berrechtigungen.",
                res.message.guild.id,
            )
            return
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
                embed = await get_page(message=res.message, page=res.component.id[5:])
                await res.respond(
                    type=7, embed=embed, components=await get_help_buttons(res.message)
                )
                await log(
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
                                style=await get_buttoncolour(message=res.message),
                                label="Normal",
                                emoji="📄",
                                id="say_normal",
                                disabled=True,
                            ),
                            Button(
                                style=await get_buttoncolour(message=res.message),
                                label="Embed",
                                emoji="✒",
                                id="say_embed",
                                disabled=False,
                            ),
                        ]
                    ],
                )
                await log(
                    f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Say-Nachricht interagiert!",
                    res.message.guild.id,
                )
            elif res.component.id == "say_embed":
                embed = discord.Embed(
                    title="**Say**",
                    description=str(res.message.content),
                    colour=await get_embedcolour(res.message),
                )
                embed._footer = await get_embed_footer(message=res.message)
                embed._thumbnail = await get_embed_thumbnail()
                await res.respond(
                    type=7,
                    embed=embed,
                    content=" ",
                    components=[
                        [
                            Button(
                                style=await get_buttoncolour(message=res.message),
                                label="Normal",
                                emoji="📄",
                                id="say_normal",
                                disabled=False,
                            ),
                            Button(
                                style=await get_buttoncolour(message=res.message),
                                label="Embed",
                                emoji="✒",
                                id="say_embed",
                                disabled=True,
                            ),
                        ]
                    ],
                )
                await log(
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
                    default_button_array = await get_calculator_buttons(res.message)
                    final_button_array, cache_array = [], []
                    for array in default_button_array:
                        for button in array:
                            button._disabled = True
                            cache_array.append(button)
                        final_button_array.append(cache_array)
                        cache_array = []
                    await res.respond(
                        type=7,
                        content="Rechner geschlossen!",
                        components=final_button_array)
                    return
                elif res.component.label == "⌫":
                    description = description[:-2] + "|"
                elif res.component.label == "Clear":
                    description = "|"
                elif res.component.label == "=":
                    description = str(calculate(description[:-1])) + "|"
                else:
                    description = description[:-1] + res.component.label + "|"
                description = "```" + description + "```"
                embed = discord.Embed(
                    title=f"**{res.author.name}'s Rechner**",
                    description=description,
                    colour=await get_embedcolour(res.message),
                )
                embed._footer = await get_embed_footer(message=res.message)
                await res.respond(
                    type=7,
                    embed=embed,
                    components=await get_calculator_buttons(res.message)
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
