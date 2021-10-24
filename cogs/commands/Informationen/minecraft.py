import datetime

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.logging import log


class minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="mcaccount",
        aliases=["mc", "mcinfo", "accinfo", "minecraft"],
        usage="<Name / UUID>",
    )
    async def mcaccount(self, ctx: commands.Context, name: str):
        global uuid
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        if "-" in name:
            name = name.replace("-", "")
        if len(name) == 32:  # TRY UUID
            uuid = name
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    "GET", f"https://api.mojang.com/user/profiles/{uuid}/names"
                ) as response:
                    if response.status != 200:
                        embed = discord.Embed(
                            title="**Fehler**",
                            description=f"Es konnte kein Minecraft Account mit der UUID ```{uuid}``` gefunden werden!",
                            colour=await get_embedcolour(ctx.message),
                        )
                        embed.set_thumbnail(
                            url="https://media.discordapp.net/attachments/851853486948745246/896803463856553984/minecraft.png"
                        )
                        embed._footer = await get_embed_footer(ctx)
                        await ctx.send(embed=embed)
                        await log(
                            text=f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}mcaccount zu nutzen, gab aber eine ungültige UUID an!",
                            guildid=ctx.guild.id,
                        )
                        return
                    data = await response.json()
                    name = dict(data[-1])["name"]
                    name_history = await get_name_history(data)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    "GET", f"https://api.mojang.com/users/profiles/minecraft/{name}"
                ) as response:
                    if response.status != 200:
                        embed = discord.Embed(
                            title="**Fehler**",
                            description=f"Es konnte kein Minecraft Account mit dem Namen ```{name}``` gefunden werden!",
                            colour=await get_embedcolour(ctx.message),
                        )
                        embed.set_thumbnail(
                            url="https://media.discordapp.net/attachments/851853486948745246/896803463856553984/minecraft.png"
                        )
                        embed._footer = await get_embed_footer(ctx)
                        await ctx.send(embed=embed)
                        await log(
                            text=f"{time}: Der Nutzer {user} hat versucht den Befehl {await get_prefix_string(ctx.message)}mcaccount zu nutzen, gab aber einen ungültigen Namen an!",
                            guildid=ctx.guild.id,
                        )
                        return
                    data = await response.json()
                    uuid = data["id"]
                    name = data["name"]
                async with session.request(
                    "GET", f"https://api.mojang.com/user/profiles/{uuid}/names"
                ) as response:
                    data = await response.json()
                    name_history = await get_name_history(data)
        embed = discord.Embed(
            title="Minecraft Account Info", colour=await get_embedcolour(ctx.message)
        )
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="UUID", value=uuid, inline=False)
        embed.add_field(name="Name History", value=name_history, inline=False)
        embed.add_field(
            name="Links",
            value=f"[Skin Download](https://crafatar.com/skins/{uuid}) | [NameMC Profil](https://de.namemc.com/{name})",
            inline=False,
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/851853486948745246/896803463856553984/minecraft.png"
        )
        embed.set_image(url=f"https://crafatar.com/renders/body/{uuid}?overlay.png")
        embed._footer = await get_embed_footer(ctx)
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {await get_prefix_string(ctx.message)}"
            f'mcaccount mit der Eingabe "{name}" benutzt!',
            guildid=ctx.guild.id,
        )


async def get_name_history(history: list) -> str:
    history_str = ""
    for dict in history:
        history_str = (
            history_str
            + f'{dict["name"]} {"◌ <t:" + str(dict["changedToAt"])[:-3] + ":R>" if "changedToAt" in dict else ""} \n'
        )
    return history_str


########################################################################################################################


def setup(bot):
    bot.add_cog(minecraft(bot))
