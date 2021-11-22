import asyncio
import datetime
import json
import copy
import discord, os
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button

from cogs.core.config.config_botchannel import botchannel_check
from cogs.core.config.config_buttoncolour import get_buttoncolour
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail
from cogs.core.functions.func_json import writejson
from cogs.core.functions.logging import log


async def todo_file_check(path) -> None:
    data = {"todo": {"list": [], "privacy": "public"}}
    if not os.path.isfile(path):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


async def get_todo(user: discord.User) -> dict:
    path = os.path.join("data", "user", f"{user.id}.json")
    await todo_file_check(path)
    with open(path, "r") as f:
        data = json.load(f)
    return data["todo"]


class todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="todo", aliases=["tasks", "aufgaben", "todos"])
    async def todo(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.invoke(self.todo_help)

    @todo.command(name="help", aliases=["hilfe", "commands"])
    async def todo_help(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        embed = discord.Embed(
            title="**Todo Help**",
            description=f"Hier findest du alle Subbefehle zum {prefix}todo Befehl!",
            colour=await get_embedcolour(ctx.message),
        )
        embed.add_field(
            name=f"**{prefix}todo hilfe**",
            value=f"Hier siehst du alle Subbefehle zum {prefix}todo Befehl!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}todo list**",
            value=f"Zeigt alle deine aktiven Todos an!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}todo add**",
            value=f"Füge eine Todo zur Liste hinzu!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}todo remove**",
            value=f"Entferne ein TODO von der Liste!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}todo clear**",
            value=f"Lösche deine gesamte TODO-Liste!",
            inline=False,
        )
        embed.add_field(
            name=f"**{prefix}todo toggle**",
            value=f"Ändere die Sichtbarkeit deiner TODO-Liste!",
            inline=False,
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}" "todo hilfe benutzt!",
            guildid=ctx.guild.id,
        )

    @todo.command(name="list", aliases=["liste"])
    async def todo_list(self, ctx: commands.Context, member: discord.User = None):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        if not member:
            member = ctx.author
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        todo_dict = await get_todo(user=member)
        if todo_dict["privacy"] == "private" and ctx.author.id != member.id:
            embed = discord.Embed(
                title=f"**Fehler**",
                description=f"Die Todo-Liste von {member.mention} ist auf privat gestellt!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht mit dem Befehl {prefix}todo "
                f"liste die TODO-Liste von {str(member)} einzusehen, diese war aber auf privat gestellt!",
                guildid=ctx.guild.id,
            )
            return
        todos_optimized, passed = "", 1
        for item in todo_dict["list"]:
            todos_optimized += f"**{passed}.** {item}\n"
            passed += 1
        embed = discord.Embed(
            title=f"**Todo Liste von {str(member)}**",
            description=todos_optimized
            if todos_optimized != ""
            else f"Keine TODOs vorhanden. Falls du der Besitzer dieser TODO-Liste bist kannst du mit `{prefix}todo add <TODO>` hinzufügen!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"todo liste benutzt und damit die TODOs von {str(member)} eingesehen!",
            guildid=ctx.guild.id,
        )

    @todo.command(name="add", aliases=["hinzufügen"], usage="<TODO>")
    async def todo_add(self, ctx: commands.Context, *, new_todo: str):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        if len(new_todo) > 200:
            embed = discord.Embed(
                title=f"**Fehler**",
                description=f"Ein TODO darf nicht über 200 Zeichen lang sein!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht den Befehl {prefix}todo "
                f"add zu nutzen, jedoch wurde das Zeichenlimit überschritten!",
                guildid=ctx.guild.id,
            )
            return
        path = os.path.join("data", "user", f"{ctx.author.id}.json")
        with open(path, "r") as f:
            data = json.load(f)
            data["todo"]["list"].append(new_todo)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(
            title=f"**Todo Add**",
            description=f"Der Eintrag `{new_todo}` wurde erfolgreich zur TODO-Liste hinzugefügt!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"todo add benutzt und damit die TODO-Liste auf {len(data['todo']['list'])} Einträge erweitert!",
            guildid=ctx.guild.id,
        )

    @todo.command(name="remove", aliases=["entfernen"], usage="<Nummer des TODO>")
    async def todo_remove(self, ctx: commands.Context, number: int):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "user", f"{ctx.author.id}.json")
        with open(path, "r") as f:
            data = json.load(f)
            backup = copy.deepcopy(data)
            todos = data["todo"]["list"]
        try:
            todos[number - 1]
        except Exception:
            embed = discord.Embed(
                title=f"**Fehler**",
                description=f"Es existiert kein TODO mit der Nummer **{number}**!",
                colour=await get_embedcolour(ctx.message),
            )
            embed._footer = await get_embed_footer(ctx)
            embed._thumbnail = await get_embed_thumbnail()
            await ctx.send(embed=embed)
            await log(
                text=f"{time}: Der Nutzer {user} hat versucht den Befehl {prefix}todo "
                f"remove zu nutzen, jedoch wurde kein TODO mit der angegebenen Nummer gefunden!",
                guildid=ctx.guild.id,
            )
            return
        data["todo"]["list"].pop(number - 1)
        await writejson(key="todo", value=data["todo"], path=path)
        embed = discord.Embed(
            title=f"**Todo Remove**",
            description=f"Der Eintrag mit der Nummer **{number}** wurde erfolgreich von der TODO-Liste entfernt!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        msg = await ctx.send(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(ctx.message),
                    label="Wiederherstellen",
                    custom_id="todo_add_undo",
                )
            ],
        )
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"todo remove benutzt und damit den {number}. Eintrag entfernt!",
            guildid=ctx.guild.id,
        )
        try:
            res = await self.bot.wait_for(
                event="button_click",
                timeout=15.0,
                check=lambda inter: inter.custom_id == "todo_add_undo"
                and inter.message.id == msg.id
                and inter.author.id == ctx.author.id,
            )
            await writejson(key="todo", value=backup["todo"], path=path)
            await res.respond(
                content=f"Der TODO-Eintrag mit der Nummer **{number}** wurde erfolgreich wiederhergestellt!"
            )
            await log(
                f'{time}: Der Nutzer {user} hat mit dem Button "Wiederherstellen" einen TODO-Eintrag wiederhergestellt!',
                ctx.guild.id,
            )
        except asyncio.TimeoutError:
            pass
        await msg.edit(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(ctx.message),
                    label="Wiederherstellen",
                    custom_id="todo_add_undo",
                    disabled=True,
                )
            ],
        )

    @todo.command(name="clear", aliases=["delete", "löschen"])
    async def todo_clear(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "user", f"{ctx.author.id}.json")
        with open(path, "r") as f:
            data = json.load(f)
            backup = copy.deepcopy(data)
            data["todo"]["list"] = []
        await writejson(key="todo", value=data["todo"], path=path)
        embed = discord.Embed(
            title=f"**Todo Clear**",
            description=f"Deine TODO-Liste wurde erfolgreich geleert!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        msg = await ctx.send(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(ctx.message),
                    label="Wiederherstellen",
                    custom_id="todo_clear_undo",
                )
            ],
        )
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"todo clear benutzt und damit die TODO-Liste gelöscht!",
            guildid=ctx.guild.id,
        )
        try:
            res = await self.bot.wait_for(
                event="button_click",
                timeout=15.0,
                check=lambda inter: inter.custom_id == "todo_clear_undo"
                and inter.message.id == msg.id
                and inter.author.id == ctx.author.id,
            )
            await writejson(key="todo", value=backup["todo"], path=path)
            await res.respond(
                content=f"Die TODO-Liste wurde erfolgreich wiederhergestellt!"
            )
            await log(
                f'{time}: Der Nutzer {user} hat mit dem Button "Wiederherstellen" die TODO-Liste wiederhergestellt!',
                ctx.guild.id,
            )
        except asyncio.TimeoutError:
            pass
        await msg.edit(
            embed=embed,
            components=[
                Button(
                    style=await get_buttoncolour(ctx.message),
                    label="Wiederherstellen",
                    custom_id="todo_clear_undo",
                    disabled=True,
                )
            ],
        )

    @todo.command(name="toggle", aliases=["privacy", "datenschutz"])
    async def todo_toggle(self, ctx: commands.Context):
        if not await botchannel_check(ctx):
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)
            return
        time = datetime.datetime.now()
        user = ctx.author.name
        prefix = await get_prefix_string(ctx.message)
        path = os.path.join("data", "user", f"{ctx.author.id}.json")
        with open(path, "r") as f:
            data = json.load(f)
            data["todo"]["privacy"] = (
                "private" if data["todo"]["privacy"] != "private" else "public"
            )
        await writejson(key="todo", value=data["todo"], path=path)
        privacy_type = (
            "privat" if data["todo"]["privacy"] == "private" else "öffentlich"
        )
        embed = discord.Embed(
            title=f"**Todo Toggle**",
            description=f"Deine TODO-Liste ist nun auf **{privacy_type}** gestellt!",
            colour=await get_embedcolour(ctx.message),
        )
        embed._footer = await get_embed_footer(ctx)
        embed._thumbnail = await get_embed_thumbnail()
        await ctx.send(embed=embed)
        await log(
            f"{time}: Der Nutzer {user} hat den Befehl {prefix}"
            f"todo toggle benutzt und damit die TODO-Liste auf {privacy_type} gestellt!",
            guildid=ctx.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(todo(bot))
