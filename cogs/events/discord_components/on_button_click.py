import datetime
import traceback

import discord
from discord.ext import commands
from discord_components import Button

from cogs.commands.Hilfe.help import get_page
from cogs.commands.Tools.rechner import calculate
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.cache import save_embed_to_cache, get_embed_from_cache, save_message_to_cache, \
    get_messages_from_cache
from cogs.core.functions.functions import get_author
from cogs.core.functions.logging import log
from config import FOOTER, THUMBNAIL_URL, ICON_URL, CALCULATING_ERROR


class on_button_click(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, res):
        print(get_messages_from_cache(authorid=res.author.id))
        #if res.author.id not in get_messages_from_cache(authorid=res.author.id):
            #await res.respond(content="Diese Nachricht gehört dir nicht! Nutz den Befehl bitte selbst!")
            #return

        user = res.author.name
        try:
            helpp = [
                "allgemein",
                "informationen",
                "unterhaltung",
                "moderation",
                "administration",
                "übersicht",
                "inhaber",
            ]
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
            elif res.component.id == "say_normal":
                await res.respond(type=7, content=res.message.embeds[0].description, embeds=[], components=[[
                    Button(style=get_buttoncolour(message=res.message), label="Normal", emoji="📄", id="say_normal",
                           disabled=True),
                    Button(style=get_buttoncolour(message=res.message), label="Embed", emoji="✒", id="say_embed",
                           disabled=False),
                ]], )
                log(
                    f"{datetime.datetime.now()}: Der Spieler {user} hat mit der Say-Nachricht interagiert!",
                    res.message.guild.id,
                )
            elif res.component.id == "say_embed":
                embed = discord.Embed(
                    title="**Say**",
                    description=str(res.message.content),
                    colour=get_embedcolour(res.message),
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.set_footer(
                    text=FOOTER[0]
                         + str(user)
                         + FOOTER[1]
                         + str(get_author())
                         + FOOTER[2]
                         + str(get_prefix_string(res.message)),
                    icon_url=ICON_URL,
                )
                await res.respond(type=7, embed=embed, content=" ", components=[[
                    Button(style=get_buttoncolour(message=res.message), label="Normal", emoji="📄", id="say_normal",
                           disabled=False),
                    Button(style=get_buttoncolour(message=res.message), label="Embed", emoji="✒", id="say_embed",
                           disabled=True),
                ]], )
                log(
                    f"{datetime.datetime.now()}: Der Spieler {user} hat mit der Say-Nachricht interagiert!",
                    res.message.guild.id,
                )
            elif "calc_" in res.component.id:
                description = str(res.message.embeds[0].description)
                if description == CALCULATING_ERROR:
                    description = '|'
                elif res.component.label == 'Exit':
                    await res.respond(type=7, content="Rechner geschlossen!", components=[
                        [
                            Button(style=get_buttoncolour(message=res.message), label="1", id="calc_1", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="2", id="calc_2", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="3", id="calc_3", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="x", id="calc_x", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="Exit", id="calc_exit",
                                   disabled=True),
                        ],
                        [
                            Button(style=get_buttoncolour(message=res.message), label="4", id="calc_4", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="5", id="calc_5", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="6", id="calc_6", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="÷", id="calc_division",
                                   disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="⌫", id="calc_delete",
                                   disabled=True),
                        ],
                        [
                            Button(style=get_buttoncolour(message=res.message), label="7", id="calc_7", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="8", id="calc_8", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="9", id="calc_9", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="+", id="calc_addition",
                                   disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="Clear", id="calc_clear",
                                   disabled=True),
                        ],
                        [
                            Button(style=get_buttoncolour(message=res.message), label="00", id="calc_00",
                                   disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="0", id="calc_0", disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label=".", id="calc_comma",
                                   disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="-", id="calc_subtraction",
                                   disabled=True),
                            Button(style=get_buttoncolour(message=res.message), label="=", id="calc_equal",
                                   disabled=True),
                        ], ],
                                      )
                elif res.component.label == '⌫':
                    description = description[:-2] + "|"
                elif res.component.label == 'Clear':
                    description = "|"
                elif res.component.label == '=':
                    description = calculate(description[:-1])
                else:
                    description = description[:-1] + res.component.label + "|"
                embed = discord.Embed(
                    title=f"**{res.author.name}'s Rechner**", description=description,
                    colour=get_embedcolour(res.message)
                )
                embed.set_footer(
                    text=FOOTER[0]
                         + str(user)
                         + FOOTER[1]
                         + str(get_author())
                         + FOOTER[2]
                         + str(get_prefix_string(res.message)),
                    icon_url=ICON_URL,
                )
                await res.respond(type=7, embed=embed, components=[
                    [
                        Button(style=get_buttoncolour(message=res.message), label="1", id="calc_1"),
                        Button(style=get_buttoncolour(message=res.message), label="2", id="calc_2"),
                        Button(style=get_buttoncolour(message=res.message), label="3", id="calc_3"),
                        Button(style=get_buttoncolour(message=res.message), label="x", id="calc_x"),
                        Button(style=get_buttoncolour(message=res.message), label="Exit", id="calc_exit"),
                    ],
                    [
                        Button(style=get_buttoncolour(message=res.message), label="4", id="calc_4"),
                        Button(style=get_buttoncolour(message=res.message), label="5", id="calc_5"),
                        Button(style=get_buttoncolour(message=res.message), label="6", id="calc_6"),
                        Button(style=get_buttoncolour(message=res.message), label="÷", id="calc_division"),
                        Button(style=get_buttoncolour(message=res.message), label="⌫", id="calc_delete"),
                    ],
                    [
                        Button(style=get_buttoncolour(message=res.message), label="7", id="calc_7"),
                        Button(style=get_buttoncolour(message=res.message), label="8", id="calc_8"),
                        Button(style=get_buttoncolour(message=res.message), label="9", id="calc_9"),
                        Button(style=get_buttoncolour(message=res.message), label="+", id="calc_addition"),
                        Button(style=get_buttoncolour(message=res.message), label="Clear", id="calc_clear"),
                    ],
                    [
                        Button(style=get_buttoncolour(message=res.message), label="00", id="calc_00"),
                        Button(style=get_buttoncolour(message=res.message), label="0", id="calc_0"),
                        Button(style=get_buttoncolour(message=res.message), label=".", id="calc_comma"),
                        Button(style=get_buttoncolour(message=res.message), label="-", id="calc_subtraction"),
                        Button(style=get_buttoncolour(message=res.message), label="=", id="calc_equal"),
                    ], ], )
            else:
                await res.respond(
                    content=f"Error 404: Diesen Button {res.component.label} kenne ich leider nicht!", empheral=True
                )
        except Exception:
            traceback.print_exc()


########################################################################################################################


def setup(bot):
    bot.add_cog(on_button_click(bot))
