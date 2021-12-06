import datetime

import discord
import discord_components
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.cache import save_message_to_cache
from cogs.core.functions.logging import log


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["help", "commands"])
    async def hilfe(self, ctx):
        time = datetime.datetime.now()
        user = ctx.author.name
        msg2 = ctx.message
        if await botchannel_check(ctx):
            msg = await ctx.send(
                embed=await get_page(ctx.message, "übersicht"),
                components=await get_help_buttons(ctx.message),
            )
            await save_message_to_cache(message=msg, author=msg2.author)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + await get_prefix_string(ctx.message)
                + "hilfe benutzt!",
                ctx.guild.id,
            )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


async def on_help_button(interaction: discord_components.interaction):
    user = interaction.author.name
    embed = await get_page(
        message=interaction.message,
        page=interaction.component.id[5:],
        author=interaction.author,
    )
    await log(
        f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Hilfenachricht interagiert und die "
        f"Seite {interaction.component.label.lower()} aufgerufen!",
        interaction.message.guild.id,
    )
    await interaction.respond(
        type=7, embed=embed, components=await get_help_buttons(interaction.message)
    )


async def get_help_buttons(msg):
    buttoncolour = await get_buttoncolour(msg)
    buttons = [
        [
            Button(
                style=buttoncolour,
                label="    Übersicht    ",
                emoji="🔖",
                custom_id="help_übersicht",
            ),
            Button(
                style=buttoncolour,
                label="    Allgemein     ",
                emoji="🤖",
                custom_id="help_allgemein",
            ),
            Button(
                style=buttoncolour,
                label="Informationen ",
                emoji="📉",
                custom_id="help_informationen",
            ),
            Button(
                style=buttoncolour,
                label=" Unterhaltung   ‎‎‎",
                emoji="🎲",
                custom_id="help_unterhaltung",
            ),
        ],
        [
            Button(
                style=buttoncolour,
                label="       Bilder        ",
                emoji="📸",
                custom_id="help_images",
            ),
            Button(
                style=buttoncolour,
                label="     Levelling      ",
                emoji="🧪",
                custom_id="help_levelling",
            ),
            Button(
                style=buttoncolour,
                label="       Musik        ",
                emoji="🎵",
                custom_id="help_musik",
            ),
            Button(
                style=buttoncolour,
                label="       Tools         ",
                emoji="💡",
                custom_id="help_tools",
            ),
        ],
        [
            Button(
                style=buttoncolour,
                label="  Moderation    ",
                emoji="🛡",
                custom_id="help_moderation",
            ),
            Button(
                style=buttoncolour,
                label="Administration",
                emoji="⚙",
                custom_id="help_administration",
            ),
            Button(
                style=buttoncolour,
                label="       Inhaber      ",
                emoji="🔒",
                custom_id="help_inhaber",
            ),
        ],
    ]
    return buttons


async def get_page(message, page, author=None):
    if not author:
        author = message.author
    prefix = await get_prefix_string(message)
    if page == "übersicht":
        embed = discord.Embed(
            title="**Hilfe Übersicht**",
            description="Hier findest du alle Hilfekategorien!",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"`{prefix}hilfe`",
            value="Zeigt dir eine Übersicht aller Hilfekategorien!",
            inline=False,
        )
        embed.add_field(
            name=f"**Allgemein**",
            value="Hier kannst du mehr über mich erfahren!",
            inline=False,
        )
        embed.add_field(
            name=f"**Informationen**",
            value="Hier findest du alles was mit Informationen zu tun hat!",
            inline=False,
        )
        embed.add_field(
            name=f"**Unterhaltung**",
            value="Hier findest du bestimmt was gegen Langeweile oder was zum Lachen!",
            inline=False,
        )
        embed.add_field(
            name=f"**Bilder**",
            value="Hier wirst du mit vielen süßen Tierbildern versorgt!",
            inline=False,
        )
        embed.add_field(
            name=f"**Levelling**",
            value="Hier findest du alle möglichen Befehle zum Levellingsystem - flex mit deiner Aktivität!",
            inline=False,
        )
        embed.add_field(
            name=f"**Musik**",
            value="Hier findest du alle möglichen Befehle für den perfekten Hörgenuss!",
            inline=False,
        )
        embed.add_field(
            name=f"**Tools**",
            value="Ob Gewinnspiele erstellen, Taschenrechner oder QR Code Generator - hier findest du viele coole Befehle!",
            inline=False,
        )
        embed.add_field(
            name=f"**Moderation**",
            value="Ob Muten oder direkt bannen - hier findest du alles was du als Moderator brauchst.",
            inline=False,
        )
        embed.add_field(
            name=f"**Administration**",
            value="Hier gibts viele Einstellungen für die Admins des Servers!",
            inline=False,
        )
        embed.add_field(
            name=f"**Inhaber**",
            value="Hiervon kannst du wahrscheinlich nichts nutzen - außer du bist der Inhaber ;)!",
            inline=False,
        )
    elif page == "allgemein":
        embed = discord.Embed(
            title="**Hilfe Allgemein**",
            description="Hier findest du alle Befehle zu der Kategorie `Allgemein!`",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}hilfe**",
            value="Zeigt dir alle Befehle in Kategrien unterteilt an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}invite**",
            value="Invite mich oder schau bei meinem Zuhause vorbei!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}botinfo**",
            value="Zeigt dir Daten zu mir!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}ping**",
            value="Erfahre meinen aktuellen Ping!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}commandstats**",
            value="Siehe die Nutzungszahlen der Top-10 Befehle ein!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}vorschlag**",
            value="Schlage ein Feature / einen Befehl vor!",
            inline=False,
        )
    elif page == "informationen":
        embed = discord.Embed(
            title="**Hilfe Informationen**",
            description="Hier findest du alle Befehle zu der Kategorie `Informationen!`",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}serverinfo**",
            value="Zeigt Daten zum aktuellen Server an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}nutzerinfo**",
            value="Zeigt Daten zu einem Nutzer an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}duden**",
            value="Zeigt dir Informationen zu deutschen Wörtern an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}lookup**",
            value="Zeigt Daten zu einer angegebenen Domain an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}mcaccount**",
            value="Gibt Informationen über einen bestimmten Minecraft Account aus!",
            inline=False,
        )
    elif page == "unterhaltung":
        embed = discord.Embed(
            title="**Hilfe Unterhaltung**",
            description="Hier findest du alle Befehle zu der Kategorie `Unterhaltung!`",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}activities**",
            value="Schaue YouTube mit Freunden & spiele unterschiedliche Spiele direkt auf Discord!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}meme**",
            value="Zeigt dir einen zufälligen Meme" " von Reddit!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}ssp**",
            value="Spiele Schere, Stein, Papier gegen mich!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}chat**",
            value="Sprich mit mir - dabei lernst du auch noch Englisch!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}würfel**",
            value="Nutze meinen integrierten" " Würfel!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}münzwurf**",
            value="Wirf eine Münze!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}8ball**",
            value="Der Orakel beantwortet jede deiner Fragen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}löschdich**",
            value="Fordere einen bestimmten Nutzer dazu"
                  "auf, sich aus dem Internet zu "
                  "löschen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}say**",
            value="Ich spreche dir nach!",
            inline=False,
        )
    elif page == "images":
        embed = discord.Embed(
            title="**Hilfe Bilder**",
            description="Hier findest du alle Befehle zu der Kategorie `Bilder`!",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}hund**",
            value="Schau dir süße Hunde an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}katze**",
            value="Schau dir knuffige Katzen an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}ente**",
            value="Schau dir watschelnde Enten an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}fuchs**",
            value="Schau dir niedliche Füchse an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}vogel**",
            value="Schau dir kunterbunte Vögel an!",
            inline=False,
        )
    elif page == "levelling":
        embed = discord.Embed(
            title="**Hilfe Levelling**",
            description="Hier findest du alle Befehle zu der Kategorie `Levelling!`",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}rank**",
            value="Gibt Informationen zu dem Levelfortschritt des jeweiligen Nutzers!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}top**",
            value="Zeigt die Top 10 Spieler auf dem aktuellen Server an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}levelling**",
            value=f"Alle Einstellungsmöglichkeiten zum Levelsystem!",
            inline=False,
        )

    elif page == "musik":
        embed = discord.Embed(
            title="**Hilfe Musik**",
            description="Hier findest du alle Befehle zu der Kategorie `Musik`!",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}join**",
            value="Nutze diesen Befehl damit ich deinen Voichechannel betrete!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}play**",
            value="Nutze diesen Befehl um Musik abzuspielen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}pause**",
            value="Nutze diesen Befehl den aktuellen Song zu pausieren!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}pause**",
            value="Nutze diesen Befehl den pausierten Song zu fortzusetzen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}stop**",
            value="Nutze diesen Befehl um den aktuellen Song zu stoppen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}leave**",
            value="Nutze diesen Befehl damit ich deinen Voichechannel verlasse!",
            inline=False,
        )
    elif page == "tools":
        embed = discord.Embed(
            title="**Hilfe Tools**",
            description="Hier findest du alle Befehle zu der Kategorie `Tools`!",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}gewinnspiel**",
            value="Hier findest du alle Befehle zum Veranstalten des perfekten Gewinnspiels!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}rechner**",
            value="Ein fancy Rechner für einfache mathematische Probleme!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}todo**",
            value="Deine zuverlässige digitale TODO-Liste über Discord!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}screenshot**",
            value="Erstelle einen Screenshot von einer beliebigen Website!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}qr**",
            value="Erstelle einen QR Code zu einer" " beliebigen Website!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}nachricht**",
            value="Sende einen personalisierten Embed in einen Channel deiner Wahl!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}avatar**",
            value="Gib dir das Profilbild von einem Nutzer aus!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}servericon**",
            value="Gib dir das Profilbild von dem aktuellen Server aus!",
            inline=False,
        )
    elif page == "moderation":
        embed = discord.Embed(
            title="**Hilfe Moderation**",
            description="Hier findest du alle Befehle zu der Kategorie `Moderation!`",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}slowmode**",
            value="Lege den Intervall zwischen Nachrichten in einem bestimmten Kanal fest!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}clear**",
            value="Lösche eine bestimmte Anzahl and Nachrichten!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}ban**",
            value="Banne einen bestimmten Nutzer bis er entbannt wird!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}unban**",
            value="Entbanne einen zuvor gebannten Nutzer!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}kick**",
            value="Kicke einen bestimmten Nutzer!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}mute**",
            value="Stumme einen spezifischen Nutzer!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}unmute**",
            value="Entstumme einen spezifischen Nutzer!",
            inline=False,
        )
    elif page == "administration":
        embed = discord.Embed(
            title="**Hilfe Administration**",
            description="Hier findest du alle Befehle zu der Kategorie `Administrator!`",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}config**",
            value="Ändere die" " Botkonfiguration über einen Befehl!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}channelclear**",
            value="Lösche alle Nachrichten" " aus einem Channel!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}botlog**",
            value="Gebe dir den Botlog deines" " Servers aus!",
            inline=False,
        )
    elif page == "inhaber":
        embed = discord.Embed(
            title="**Hilfe Administration**",
            description="Hier findest du alle Befehle zu der Kategorie `Inhaber`!",
            colour=await get_embedcolour(message),
        )
        embed.add_field(
            name=f"**{prefix}broadcast**",
            value="Sende eine Nachricht an alle Serverowner die diesen Bot nutzen!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}cog**",
            value="Lade, Entlade, Lade einzelne oder alle " "Cogs neu!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}adminconfig**",
            value="Bearbeite die Config eines " "anderen Servers!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}adminresetconfig**",
            value="Setze eine Config zurück!",
            inline=False,
        )
    embed._footer = await get_embed_footer(message=message, author=author)
    embed._thumbnail = await get_embed_thumbnail()
    return embed


########################################################################################################################


def setup(bot):
    bot.add_cog(help(bot))
