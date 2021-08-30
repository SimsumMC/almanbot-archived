import datetime

import discord
from discord.ext import commands
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check, get_botchannel_obj_list
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embeds import get_embed_footer_text
from cogs.core.functions.cache import save_message_to_cache
from cogs.core.functions.logging import log
from config import ICON_URL, THUMBNAIL_URL, WRONG_CHANNEL_ERROR


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["help", "commands"])
    async def hilfe(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        if botchannel_check(ctx):
            msg = await ctx.send(
                embed=get_page(ctx.message, "übersicht"),
                components=get_help_buttons(ctx.message),
            )
            await save_message_to_cache(message=msg, author=msg2.author)
            log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + get_prefix_string(ctx.message)
                + "hilfe benutzt!",
                ctx.guild.id,
            )
        else:
            log(
                text=str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat probiert den Befehl "
                + get_prefix_string(ctx.message)
                + "ban im Channel #"
                + str(name)
                + " zu benutzen!",
                guildid=ctx.guild.id,
            )
            embed = discord.Embed(
                title="**Fehler**",
                description=WRONG_CHANNEL_ERROR,
                colour=get_embedcolour(message=ctx.message),
            )
            embed.set_footer(
                text=embed.set_footer(
                    text=get_embed_footer_text(ctx),
                    icon_url=ICON_URL,
                ),
                icon_url=ICON_URL,
            )
            embed.add_field(
                name="‎",
                value=get_botchannel_obj_list(ctx),
                inline=False,
            )
            await ctx.send(embed=embed)
            await msg2.delete()


def get_help_buttons(msg):
    buttons = [
        [
            Button(
                style=get_buttoncolour(msg),
                label="Übersicht",
                emoji="🔖",
                custom_id="help_übersicht",
            ),
            Button(
                style=get_buttoncolour(msg),
                label="Allgemein ",
                emoji="🤖",
                custom_id="help_allgemein",
            ),
            Button(
                style=get_buttoncolour(msg),
                label="Informationen",
                emoji="📉",
                custom_id="help_informationen",
            ),
            Button(
                style=get_buttoncolour(msg),
                label=" Unterhaltung ",
                emoji="🎲",
                custom_id="help_unterhaltung",
            ),
        ],
        [
            Button(
                style=get_buttoncolour(msg),
                label="   Musik   ",
                emoji="🎵",
                custom_id="help_musik",
            ),
            Button(
                style=get_buttoncolour(msg),
                label="    Tools    ",
                emoji="💡",
                custom_id="help_tools",
            ),
            Button(
                style=get_buttoncolour(msg),
                label="  Moderation  ",
                emoji="🛡",
                custom_id="help_moderation",
            ),
            Button(
                style=get_buttoncolour(msg),
                label="Administration",
                emoji="⚙",
                custom_id="help_administration",
            ),
        ],
        [
            Button(
                style=get_buttoncolour(msg),
                label="  Inhaber  ",
                emoji="🔒",
                custom_id="help_inhaber",
            ),
        ],
    ]
    return buttons


def get_page(message, page):
    if page == "übersicht":
        embed = discord.Embed(
            title="**Hilfe Übersicht**",
            description="Hier findest du alle Hilfekategorien!",
            colour=get_embedcolour(message),
        )
        embed.add_field(
            name=f"`{get_prefix_string(message)}hilfe`",
            value="Zeigt dir eine Übersicht aller Hilfekategorien!",
            inline=False,
        )
        embed.add_field(
            name=f"**Allgemein**",
            value="Hier findest du ein paar nützliche Befehle wenn du mich magst!",
            inline=False,
        )
        embed.add_field(
            name=f"**Informationen**",
            value="Du brauchst Informationen oder Profilbilder? Hier bekommst du sie!",
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
        embed.add_field(
            name=f"**Inhaber**",
            value="Hiervon kannst du eh nichts nutzen... :c",
            inline=False,
        )
    elif page == "allgemein":
        embed = discord.Embed(
            title="**Hilfe Allgemein**",
            description="Hier findest du alle Befehle zu der Kategorie `Allgemein!`",
            colour=get_embedcolour(message),
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
            name=f"**{get_prefix_string(message)}botinfo**",
            value="Zeigt dir Daten zu mir!",
            inline=False,
        )
    elif page == "informationen":
        embed = discord.Embed(
            title="**Hilfe Informationen**",
            description="Hier findest du alle Befehle zu der Kategorie `Informationen!`",
            colour=get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}ping**",
            value="Zeigt dir meinen Ping an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}serverinfo**",
            value="Zeigt Daten zum aktuellen Server an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}nutzerinfo**",
            value="Zeigt Daten zu einem Nutzer an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}lookup**",
            value="Zeigt Daten zu einer angegebenen Domain an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}avatar**",
            value="Gib dir das Profilbild von einem Nutzer aus!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}servericon**",
            value="Gib dir das Icon des aktuellen Servers aus!",
            inline=False,
        )
    elif page == "unterhaltung":
        embed = discord.Embed(
            title="**Hilfe Unterhaltung**",
            description="Hier findest du alle Befehle zu der Kategorie `Unterhaltung!`",
            colour=get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}meme**",
            value="Zeigt dir einen zufälligen Meme" " von Reddit!",
            inline=False,
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
            value="Spiele Schere, Stein, Papier gegen mich!",
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
            name=f"**{get_prefix_string(message)}say**",
            value="Ich spreche dir nach!",
            inline=False,
        )
    elif page == "musik":
        embed = discord.Embed(
            title="**Hilfe Musik**",
            description="Hier findest du alle Befehle zu der Kategorie `Musik`!",
            colour=get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}join**",
            value="Damit der Bot in deinen Voicechannel kommt!",
            inline=False,
        )
    elif page == "tools":
        embed = discord.Embed(
            title="**Hilfe Tools**",
            description="Hier findest du alle Befehle zu der Kategorie `Tools`!",
            colour=get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}qr**",
            value="Erstelle einen QR Code zu einer" " beliebigen Website!",
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
        embed.add_field(
            name=f"**{get_prefix_string(message)}rechner**",
            value="Ein fancy Rechner für einfache mathematische Probleme!",
            inline=False,
        )
    elif page == "moderation":
        embed = discord.Embed(
            title="**Hilfe Moderation**",
            description="Hier findest du alle Befehle zu der Kategorie `Moderation!`",
            colour=get_embedcolour(message),
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
            value="Banne einen bestimmten Nutzer bis" " er entbannt wird!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}unban**",
            value="Entbanne einen zuvor" " gebannten Nutzer!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}kick**",
            value="Kicke einen bestimmten Nutzer!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}mute**",
            value="Stumme einen spezifischen Nutzer!",
            inline=False,
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}unmute**",
            value="Entstumme einen spezifischen Nutzer!",
            inline=False,
        )
    elif page == "administration":
        embed = discord.Embed(
            title="**Hilfe Administration**",
            description="Hier findest du alle Befehle zu der Kategorie `Administrator!`",
            colour=get_embedcolour(message),
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
            colour=get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{get_prefix_string(message)}broadcast**",
            value="Sende eine Nachricht an alle Serverowner die diesen Bot nutzen!",
            inline=False,
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
            name=f"**{get_prefix_string(message)}adminctxetconfig**",
            value="Setze eine Config zurück!",
            inline=False,
        )
    embed.set_footer(
        text=get_embed_footer_text(message=message),
        icon_url=ICON_URL,
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    return embed


########################################################################################################################


def setup(bot):
    bot.add_cog(help(bot))
