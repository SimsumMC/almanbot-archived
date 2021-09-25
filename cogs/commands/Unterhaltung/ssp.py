import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button
import discord_components
from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.cache import save_message_to_cache
from cogs.core.functions.logging import log


class ssp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="", aliases=[], usage="")
    async def ssp(self, ctx):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        embed = discord.Embed(
            title="Schere Stein Papier",
            description="Wähle ein Werkzeug mit einem der unteren Buttons aus!\n"
            "Hinweis:\n"
            "_Bei Unentschieden wird keinem ein Punkt abgerechnet, "
            "das Spiel endet wenn jemand 3 Punkte hat._",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name=f"**Bot  0 : 0 {ctx.author.name}**", value="‎\n", inline=False
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        msg = await ctx.send(embed=embed, components=await get_ssp_buttons(ctx))
        await save_message_to_cache(message=msg, author=ctx.author)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            "ssp benutzt!",
            guildid=ctx.guild.id,
        )


async def on_ssp_button(interaction: discord_components.interaction):
    player_win = ["schere-papier", "stein-schere", "papier-stein"]
    punktestand_bot = int(interaction.message.embeds[0].fields[0].name.split(" ")[2])
    punktestand_spieler = int(
        interaction.message.embeds[0].fields[0].name.split(" ")[4]
    )
    emoji1, emoji2 = "", ""
    options = ["schere", "stein", "papier"]
    bot_choice = random.choice(options)
    player_choice = interaction.component.label.lower()
    if player_choice == bot_choice:
        pass
    elif player_choice + "-" + bot_choice in player_win:  # player won
        punktestand_spieler += 1
    else:
        punktestand_bot += 1

    if punktestand_bot == 3:
        emoji1 = "🏆"
        buttons = await get_ssp_buttons(message=interaction.message, disabled=True)
    elif punktestand_spieler == 3:
        emoji2 = "🏆"
        buttons = await get_ssp_buttons(message=interaction.message, disabled=True)
    else:
        buttons = await get_ssp_buttons(message=interaction.message)
    choice_anzeige = f"{bot_choice.capitalize()} - {player_choice.capitalize()}"
    punktestand_field = f"**Bot {emoji1} {punktestand_bot} : {punktestand_spieler} {interaction.author.name} {emoji2}**"
    embed = discord.Embed(
        title="Schere Stein Papier",
        description=interaction.message.embeds[0].description,
        colour=await get_embedcolour(interaction.message),
    )
    embed.add_field(name=punktestand_field, value=choice_anzeige + "\n", inline=False)
    embed._footer = await get_embed_footer(
        message=interaction.message, author=interaction.author
    )
    embed._thumbnail = await get_embed_thumbnail()
    await interaction.respond(type=7, embed=embed, components=buttons)
    await log(
        f"{datetime.datetime.now()}: Der Nutzer {interaction.author.name} hat mit der Schere Stein Papier-Nachricht interagiert!",
        interaction.message.guild.id,
    )


async def get_ssp_buttons(ctx=None, message=None, disabled=False):
    if ctx:
        message = ctx.message
    buttons = [
        [
            Button(
                style=await get_buttoncolour(message),
                label="Schere",
                emoji="✂",
                custom_id="ssp_scissors",
            ),
            Button(
                style=await get_buttoncolour(message),
                label="Stein",
                emoji="🪨",
                custom_id="ssp_stone",
            ),
            Button(
                style=await get_buttoncolour(message),
                label="Papier",
                emoji="📄",
                custom_id="ssp_paper",
            ),
        ],
    ]
    if disabled:
        final_button_array, cache_array = [], []
        for array in buttons:
            for button in array:
                button._disabled = True
                cache_array.append(button)
            final_button_array.append(cache_array)
            cache_array = []
    return buttons


########################################################################################################################


def setup(bot):
    bot.add_cog(ssp(bot))
