import datetime
import json
import os
from shutil import copyfile
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from cogs.commands.Hilfe.help import get_page
from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
)
from cogs.core.functions.automaticdelete import add_automaticdelete
from cogs.core.config.config_colours import get_colour
from cogs.core.functions.logging import log
from discord_components import Button, ButtonStyle, InteractionType

from cogs.core.config.config_general import get_defaultconfig


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.now()
        user = ctx.author.name
        mention = ctx.author.mention
        msg = ctx.message.content
        msg2 = ctx.message
        name = ctx.channel.name
        if isinstance(error, CommandNotFound):
            return
            # out of function for verifying on top.gg
            if botchannel_check(ctx):
                embed = discord.Embed(
                    title="Fehler",
                    description='Der Befehl "' + str(msg) + '" existiert nicht!',
                    color=get_colour(ctx.message),
                )
                embed.set_footer(
                    text="for "
                    + str(user)
                    + " | by "
                    + str(get_author())
                    + " | Prefix "
                    + get_prefix_string(message=ctx.message),
                    icon_url="https://media.discordapp.net/attachments/645276319311200286"
                    "/803322491480178739"
                    "/winging-easy.png?width=676&height=676",
                )
                await ctx.send(embed=embed)
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat probiert den ungültigen Befehl "'
                    + str(msg)
                    + '" zu nutzen!',
                    id=ctx.guild.id,
                )
            else:
                log(
                    input=str(time)
                    + ": Der Spieler "
                    + str(user)
                    + ' hat probiert den ungültigen Befehl "'
                    + str(msg)
                    + '" zu nutzen!',
                    id=ctx.guild.id,
                )
                await ctx.send(
                    str(mention)
                    + ", dieser Befehl kann nur im Kanal #{} genutzt werden.".format(
                        channel
                    ),
                    delete_after=3,
                )
                await msg2.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        path = os.path.join("data", "configs", f"{guild.id}.json")
        pathcheck = os.path.join("data", "configs", "deleted", f"{guild.id}.json")
        # config
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
        else:
            with open(path, "w") as f:
                data = get_defaultconfig()
                json.dump(data, f, indent=4)
        # logs
        path = os.path.join("data", "logs", f"{guild.id}.txt")
        pathcheck = os.path.join("data", "logs", "deleted", f"{guild.id}.txt")
        if os.path.isfile(pathcheck):
            copyfile(pathcheck, path)
            os.remove(pathcheck)
        else:
            log(
                f"{datetime.datetime.now()}: Der Bot ist dem Server beigetreten.",
                guild.id,
            )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        path = os.path.join("data", "configs", f"{guild.id}.json")
        path2 = os.path.join("data", "logs", f"{guild.id}.txt")
        dest = os.path.join("data", "configs", "deleted", f"{guild.id}.json")
        dest2 = os.path.join("data", "logs", "deleted", f"{guild.id}.txt")
        copyfile(path, dest)
        copyfile(path2, dest2)
        os.remove(path)
        os.remove(path2)
        add_automaticdelete(guild.id)

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
                            Button(style=ButtonStyle.red, label="Übersicht", emoji="🔖"),
                            Button(style=ButtonStyle.red, label="Allgemein", emoji="🤖"),
                            Button(
                                style=ButtonStyle.red, label="Informationen", emoji="📉"
                            ),
                            Button(
                                style=ButtonStyle.red, label="Unterhaltung", emoji="🎲"
                            ),
                        ],
                        [
                            Button(
                                style=ButtonStyle.red, label="Moderation", emoji="🛡"
                            ),
                            Button(
                                style=ButtonStyle.red, label="Administration", emoji="⚙"
                            ),
                            Button(style=ButtonStyle.red, label="Inhaber", emoji="🔒"),
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
    bot.add_cog(events(bot))
