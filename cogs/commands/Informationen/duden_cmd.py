import datetime
import duden
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class duden_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="duden", aliases=["wort"], usage="<Wort>")
    async def duden(self, ctx: commands.Context, word):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        try:
            w = duden.get(str(word))
            if not w:
                w = duden.get(str((word.lower()).capitalize()))
                if w:
                    pass
                else:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=f"Das Wort ```{word}``` konnte nicht gefunden werden! \nEntweder es existiert nicht oder es gab einen Fehler bei der Suche - das kann unter bestimmten Umständen vorkommen, diese sind bekannt. Das wird im nächsten Update behoben ;)",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._thumbnail = await get_embed_thumbnail()
                    embed._footer = await get_embed_footer(ctx)
                    await ctx.send(embed=embed)
                    await log(
                        text=f'{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}duden Informationen über das Wort "{word}" zu bekommen, dieses konnte aber nicht gefunden werden!',
                        guildid=ctx.guild.id,
                    )
                    return
            word_type = w.part_of_speech.split(",")[0]
            if word_type == "Substantiv":
                embed = discord.Embed(
                    title=f"Duden | {w.title}",
                    description=f"Hier findest du alle Informationen zu dem Substantiv `{word}`!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed.add_field(name="Name", value=w.name, inline=False)
                embed.add_field(name="Artikel", value=w.article, inline=False)
                embed.add_field(
                    name="Geschlecht",
                    value=str(w.part_of_speech.split(", ")[1]),
                    inline=False,
                )
                embed.add_field(
                    name="Häufigkeit von 1-5",
                    value=f"{await get_frequency(w.frequency, 5)} ({w.frequency})",
                    inline=False,
                )
                embed.add_field(
                    name="Nutzung", value=w.usage if not None else "-", inline=False
                )
                embed.add_field(
                    name="Silbentrennung",
                    value="".join([silbe + " · " for silbe in w.word_separation])[:-3],
                    inline=False,
                )
                embed.add_field(
                    name="Bedeutung",
                    value=(
                        "".join(
                            [m.replace("\n", " ") + ", " for m in w.meaning_overview]
                        )[:-2]
                        if isinstance(w.meaning_overview, list)
                        else str(w.meaning_overview)
                    )
                    if not ""
                    else "-",
                    inline=False,
                )
                embed.add_field(
                    name="Synonyme",
                    value="".join([synonym for synonym in w.synonyms])
                    if w.synonyms
                    else "-",
                    inline=False,
                )
                embed.add_field(
                    name="Herkunft", value=w.origin if not None else "-", inline=False
                )
            if "Verb" in word_type:
                embed = discord.Embed(
                    title=f"Duden | {w.title}",
                    description=f"Hier findest du alle Informationen zu dem Verb `{word}`!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed.add_field(name="Name", value=w.name, inline=False)
                embed.add_field(name="Typ", value=str(w.part_of_speech), inline=False)
                embed.add_field(
                    name="Häufigkeit von 1-5",
                    value=f"{await get_frequency(w.frequency, 5)} ({w.frequency})"
                    if w.frequency
                    else "-",
                    inline=False,
                )
                embed.add_field(
                    name="Silbentrennung",
                    value="".join([silbe + " · " for silbe in w.word_separation])[:-3],
                    inline=False,
                )
                embed.add_field(
                    name="Synonyme",
                    value="".join([synonym for synonym in w.synonyms])
                    if not None
                    else "-",
                    inline=False,
                )
                embed.add_field(
                    name="Herkunft", value=w.origin if not None else "-", inline=False
                )
            if word_type == "Adjektiv":
                embed = discord.Embed(
                    title=f"Duden | {w.title}",
                    description=f"Hier findest du alle Informationen zu dem Adjektiv `{word}`!",
                    colour=await get_embedcolour(ctx.message),
                )
                embed.add_field(name="Name", value=w.name, inline=False)
                embed.add_field(
                    name="Häufigkeit von 1-5",
                    value=f"{await get_frequency(w.frequency, 5)} ({w.frequency})"
                    if w.frequency
                    else "-",
                    inline=False,
                )
                embed.add_field(
                    name="Silbentrennung",
                    value="".join([silbe + " · " for silbe in w.word_separation])[:-3],
                    inline=False,
                )
                embed.add_field(
                    name="Synonyme",
                    value="".join([synonym for synonym in w.synonyms])
                    if not None
                    else "-",
                    inline=False,
                )
                embed.add_field(
                    name="Herkunft", value=w.origin if not None else "-", inline=False
                )
            embed._footer = await get_embed_footer(ctx)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/851853486948745246/895023337103822898/Duden_FB_Profilbild.png?width=676&height=676"
            )
            await ctx.send(embed=embed)
            await log(
                f"{time}: Der Nutzer {user} hat mit dem Befehl {await get_prefix_string(ctx.message)}"
                f'duden Informationen zum Wort "{word}" erhalten!',
                guildid=ctx.guild.id,
            )
        except Exception:
            embed = discord.Embed(
                title="**Fehler**",
                description=f"Das Wort ```{word}``` konnte nicht gefunden werden! \nEntweder es existiert nicht oder es gab einen Fehler bei der Suche - das kann unter bestimmten Umständen vorkommen, diese sind bekannt. Das wird im nächsten Update behoben ;)",
                colour=await get_embedcolour(ctx.message),
            )
            embed._thumbnail = await get_embed_thumbnail()
            embed._footer = await get_embed_footer(ctx)
            await ctx.send(embed=embed)
            await log(
                text=f'{time}: Der Nutzer {user} hat versucht mit dem Befehl {await get_prefix_string(ctx.message)}duden Informationen über das Wort "{word}" zu bekommen, dieses konnte aber nicht gefunden werden!',
                guildid=ctx.guild.id,
            )


async def get_frequency(value: int, maximum: int):
    maximum -= value
    string = ""
    for x in range(value):
        string = string + "🟥"
    for y in range(maximum):
        string = string + "⬜"
    return string


########################################################################################################################


def setup(bot):
    bot.add_cog(duden_cmd(bot))
