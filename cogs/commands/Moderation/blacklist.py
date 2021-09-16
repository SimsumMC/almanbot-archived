import datetime
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_thumbnail, get_embed_footer
from cogs.core.functions.func_json import writejson, readjson
from cogs.core.functions.logging import log


class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="blacklist",
        aliases=["wordlist"],
    )
    @commands.has_permissions(ban_members=True)
    async def blacklist(self, ctx, cmd, *, word):
        time = datetime.datetime.now()
        user = ctx.author.name
        msg2 = ctx.message
        path = os.path.join("data", "configs", f"{ctx.guild.id}.json")
        bannedWords = readjson(key="blacklist", path=path)
        if botchannel_check(ctx):
            if cmd.lower() == "add":
                if word.lower() in bannedWords:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=f"Das Wort ```{word}```"
                        " ist bereits auf der Blacklist!",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
                    await log(
                        f'{time}: Der Moderator {user} hat versucht das Wort "{word}" zur Blacklist hinzufügen,'
                        " es war aber schon drauf.",
                        guildid=ctx.guild.id,
                    )
                else:
                    await writejson(
                        type="blacklist", input=word.lower(), path=path, mode="append"
                    )
                    await msg2.delete()
                    embed = discord.Embed(
                        title="**Blacklist**",
                        description=f"Das Wort ```{word}```"
                        " wurde zur Blacklist hinzugefügt!",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
                    await log(
                        f'{time}: Der Moderator {user} hat das Wort "{word}" auf die Blacklist hinzugefügt.',
                        guildid=ctx.guild.id,
                    )
            elif cmd.lower() == "remove":
                if word.lower() in bannedWords:
                    await writejson(
                        type="blacklist", input=word.lower(), path=path, mode="removed"
                    )
                    await ctx.message.delete()
                    embed = discord.Embed(
                        title="**Blacklist**",
                        description=f"Das Wort ```{word}```"
                        " wurde von der Blacklist entfernt!",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._footer = await get_embed_footer(ctx)
                    embed._thumbnail = await get_embed_thumbnail()
                    await ctx.send(embed=embed)
                    await log(
                        f'{time}: Der Moderator {user} hat das Wort "{word}"von der Blacklist entfernt.',
                        guildid=ctx.guild.id,
                    )
                else:
                    embed = discord.Embed(
                        title="**Fehler**",
                        description=f"Das Wort ```{word}```"
                        " befindet sich nicht auf der Blacklist!",
                        colour=await get_embedcolour(ctx.message),
                    )
                    embed._thumbnail = await get_embed_thumbnail()
                    embed._footer = await get_embed_footer(ctx)
                    await ctx.send(embed=embed)
                    await log(
                        f'{time}: Der Moderator {user} hat versucht das Wort "{word}" von der Blacklist zu entfernen,'
                        " es war aber nicht drauf.",
                        guildid=ctx.guild.id,
                    )
            else:
                embed = discord.Embed(
                    title="**Fehler**", colour=await get_embedcolour(ctx.message)
                )
                embed._footer = await get_embed_footer(ctx)
                embed._thumbnail = await get_embed_thumbnail()
                embed.add_field(
                    name="‎",
                    value="Du hast ein ungültiges Argument angegeben, Nutzung: ```"
                    + await get_prefix_string(ctx.message)
                    + "blacklist <add/new>```",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await log(
                    f"{time}: Der Moderator {user} hat ein ungültiges Argument beim Befehl"
                    + await get_prefix_string(ctx.message)
                    + "blacklist eingegeben.",
                    ctx.guild.id,
                )
        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(blacklist(bot))
