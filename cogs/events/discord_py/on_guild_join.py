import datetime
import json
import os
from shutil import copyfile

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_general import get_defaultconfig
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.logging import log
from config import TESTING_MODE, TESTING_GUILDS, TOPGG_LINK


class on_guild_join(commands.Cog):
    def __init__(self, bot):
        self.guild = None
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if TESTING_MODE is True:
            if guild.id not in TESTING_GUILDS:
                await guild.leave()
                print(
                    f"TEST_MODE is True! Left server with ID {guild.id} and Name {guild.name} "
                    f"because it was not marked as a testing server."
                )
                return
        path = os.path.join("data", "configs", f"{guild.id}.json")
        pathcheck = os.path.join("data", "configs", "deleted", f"{guild.id}.json")
        # config
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
        else:
            with open(path, "w") as f:
                data = await get_defaultconfig()
                json.dump(data, f, indent=4)
        # logs
        path = os.path.join("data", "logs", f"{guild.id}.txt")
        pathcheck = os.path.join("data", "logs", "deleted", f"{guild.id}.txt")
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
            await log(
                f"{datetime.datetime.now()}: Der Bot ist dem Server erneut beigetreten.",
                guild.id,
            )
        else:
            await log(
                f"{datetime.datetime.now()}: Der Bot ist dem Server beigetreten.",
                guild.id,
            )
        prefix = await get_prefix_string(guild=guild)
        embed = discord.Embed(
            title="**Danke fürs hinzufügen!**",
            colour=await get_embedcolour(guild=guild),
            description=f"Vielen Dank das du dich für den Alman Bot entschieden hast! Du kannst alle Befehle mit `{await get_prefix_string(guild=guild)}hilfe`"
            f" sehen. \n\n"
            f"**Einrichtung**\n\n"
            f"Du kannst viele verschiedene Sachen konfigurieren, also selber entscheiden was dir am besten gefällt. Die meisten"
            f" Möglichkeiten findest du mit `{prefix}config`, du kannst aber auch die Blacklist (`{prefix}blacklist`) "
            f"sowie die Trigger (`{prefix}trigger`) verändern.\n\n"
            f"**Empfehlung**\n\n"
            f"Es macht immer Sinn, Kanäle festzulegen wo die Befehle genutzt werden dürfen - somit werden die Chats nicht vollgemüllt. "
            f'Diese kannst du ganz einfach mit dem `{prefix}config botchannel` bzw. `{prefix}config memechannel` Befehl einstellen, hierbei steht "botchannel" für'
            f' alle Befehle (Config Befehle können überall von Administratoren benutzt werden) und "memechannel" für alle Meme(-verwandten) Befehle!\n\n'
            f"**Allgemeines zur Benutzung**\n\n"
            f"Indem du mich mit @ erwähnst, bekommst du immer meinen aktuellen Prefix ausgegeben. "
            f"Um mehr zur Benutzung eines Befehls zu erfahren, gib diesen einfach ohne Argumente ein!\n\n"
            f"**Wichtiges für Administratoren / Moderatoren**\n\n"
            f"Mit dem Befehl a!botlog kannst du alle mit dem Bot genutzten Befehle / Interaktionen einsehen. Alle für die Moderatoren relevanten "
            f'Befehle können selbsterklärend unter der Kategorie "Moderation" beim Hilfe-Befehl gefunden werden.\n\n'
            f"**Bewertung**\n\n"
            f"Ich freue mich über jedes Feedback, wäre cool wenn du dir kurz die Zeit nehmen könntest und eine Bewertung bei top.gg dalassen könntest. "
            f"Klick dazu einfach auf den unteren Button!\n\n"
            f"Viel Spaß mit dem Bot!",
        )
        embed._thumbnail = await get_embed_thumbnail()
        embed._footer = await get_embed_footer(author=guild.owner, dm=True)
        await guild.owner.send(
            embed=embed,
            components=[
                Button(style=ButtonStyle.URL, label="Bewerten", url=TOPGG_LINK),
            ],
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(on_guild_join(bot))
