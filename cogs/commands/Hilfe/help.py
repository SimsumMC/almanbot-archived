import datetime

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from config import ICON_URL, THUMBNAIL_URL, FOOTER, WRONG_CHANNEL_ERROR
from cogs.core.functions.functions import (
    get_author,
    get_prefix_string,
)
from cogs.core.config.config_colours import get_colour
from cogs.core.functions.logging import log


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["help", "commands"])
    async def hilfe(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        mention = ctx.author.mention
        if botchannel_check(ctx):
            await ctx.send(
                embed=get_page(ctx.message, ctx.author.name, "übersicht"),
                components=[
                    [
                        Button(style=ButtonStyle.red, label="Übersicht", emoji="🔖"),
                        Button(style=ButtonStyle.red, label="Allgemein", emoji="🤖"),
                        Button(style=ButtonStyle.red, label="Informationen", emoji="📉"),
                        Button(style=ButtonStyle.red, label="Unterhaltung", emoji="🎲"),
                    ],
                    [
                        Button(style=ButtonStyle.red, label="Moderation", emoji="🛡"),
                        Button(
                            style=ButtonStyle.red, label="Administration", emoji="⚙"
                        ),
                        Button(style=ButtonStyle.red, label="Inhaber", emoji="🔒"),
                    ],
                ],
            )
            log(
                str(time)
                + ": Der Spieler "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "hilfe benutzt!",
                ctx.guild.id,
            )
        else:
            log(
                input=str(time)
                + ": Der Spieler "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "ban im Channel #"
                + str(name)
                + " zu benutzen!",
                id=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**", description=WRONG_CHANNEL_ERROR, colour=get_colour(message=ctx.message)
            )
            embed.set_footer(
                text=FOOTER[0]
                     + str(user)
                     + FOOTER[1]
                     + str(get_author())
                     + FOOTER[2]
                     + str(get_prefix_string(ctx.message)),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()


def get_page(message, user, page):
    if page == "übersicht":
        embed = discord.Embed(
            title="**Hilfe Übersicht**",
            description="Hier findest du alle Hilfekategorien!",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"`{get_prefix_string(message)}hilfe`",
            value="Zeigt dir eine Übersicht aller" " Hilfekategorien!",
            inline=False,
        )
        embed.add_field(
            name=f"**Allgemein**",
            value="Hier findest du ein paar nützliche Befehle!",
            inline=False,
        )
        embed.add_field(
            name=f"**Informationen**",
            value="Du brauchst Informationen? Hier bekommst du sie!",
            inline=False,
        )
        embed.add_field(
            name=f"**Unterhaltung**",
            value="Hier dreht sich alles ums Spaß haben!",
            inline=False,
        )
        embed.add_field(
            name=f"**Moderation**",
            value="Ob Muten oder direkt bannen - hier findest du alles was du als Moderator brauchst.",
            inline=False,
        )
        embed.add_field(
            name=f"**Administration**",
            value="Hier gibts noch viele Einstellungen für die Admins!",
            inline=False,
        )
    elif page == "allgemein":
        embed = discord.Embed(
            title="**Hilfe Allgemein**",
            description="Hier findest du alle Befehle zu der Kategorie `Allgemein!`",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}hilfe**",
            value="Zeigt dir eine Übersicht aller" " Hilfeseiten!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}invite**",
            value="Invite mich oder schau bei meinem Zuhause vorbei!",
            inline=False,
        )

        embed.add_field(
            name=f"**{get_prefix_string(message)}qr**",
            value="Erstelle einen QR Code zu einer" " beliebigen Website!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}avatar**",
            value="Gib dir das Profilbild von einem Nutzer aus!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}servericon**",
            value="Gib dir das Profilbild von dem aktuellen Server aus!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}nachricht**",
            value="Sende einen personalisierten Embed in einen Channel deiner Wahl!",
            inline=False,
        )
    elif page == "informationen":
        embed = discord.Embed(
            title="**Hilfe Informationen**",
            description="Hier findest du alle Befehle zu der Kategorie `Informationen!`",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}ping**",
            value="Zeigt dir meinen Ping an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}botinfo**",
            value="Zeigt dir Daten zu mir!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}serverinfo**",
            value="Zeigt Daten zum aktuellen Server an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}nutzerinfo**",
            value="Zeigt Daten zu einem Spieler an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}lookup**",
            value="Zeigt Daten zu einer angegebenen Domain an!",
            inline=False,
        )
    elif page == "unterhaltung":
        embed = discord.Embed(
            title="**Hilfe Unterhaltung**",
            description="Hier findest du alle Befehle zu der Kategorie `Unterhaltung!`",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}würfel**",
            value="Nutze meinen integrierten" " Würfel!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}münzwurf**",
            value="Wirf eine Münze!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}ssp**",
            value="Spiele Schere, Stein, Papier gegen" " mich!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}löschdich**",
            value="Fordere einen bestimmten Nutzer dazu"
            "auf, sich aus dem Internet zu "
            "löschen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}meme**",
            value="Zeigt dir einen zufälligen Meme" " von Reddit!",
            inline=False,
        )
    elif page == "moderation":
        embed = discord.Embed(
            title="**Hilfe Moderation**",
            description="Hier findest du alle Befehle zu der Kategorie `Moderation!`",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}slowmode**",
            value="Lege den Intervall zwischen Nachrichten in einem bestimmten Kanal fest.!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}clear**",
            value="Lösche eine bestimmte Anzahl an" " Nachrichten!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}ban**",
            value="Banne einen bestimmten Spieler bis" " er entbannt wird!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}unban**",
            value="Entbanne einen zuvor" " gebannten Spieler!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}kick**",
            value="Kicke einen bestimmten Spieler!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}mute**",
            value="Stumme einen spezifischen Spieler!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}unmute**",
            value="Entstumme einen spezifischen Spieler!",
            inline=False,
        )
    elif page == "administration":
        embed = discord.Embed(
            title="**Hilfe Administration**",
            description="Hier findest du alle Befehle zu der Kategorie `Administrator!`",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}config**",
            value="Ändere die" " Botkonfiguration über einen Befehl!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}channelclear**",
            value="Lösche alle Nachrichten" " aus einem Channel!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}botlog**",
            value="Gebe dir den Botlog deines" " Servers aus!",
            inline=False,
        )
    elif page == "inhaber":
        embed = discord.Embed(
            title="**Hilfe Administration**",
            description="Hier findest du alle Befehle zu der Kategorie `Inhaber`!",
            colour=get_colour(message),
        )
        embed.set_footer(
            text=FOOTER[0]
            + str(user)
            + FOOTER[1]
            + str(get_author())
            + FOOTER[2]
            + str(get_prefix_string(message)),
            icon_url=ICON_URL,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}cog**",
            value="Lade, Entlade, Lade einzelne oder alle " "Cogs neu!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}adminconfig**",
            value="Bearbeite die Config eines " "anderen Servers!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}adminresetconfig**",
            value="Setze eine Config zurück!",
            inline=False,
        )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    return embed


########################################################################################################################


def setup(bot):
    bot.add_cog(help(bot))
