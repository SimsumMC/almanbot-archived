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
from main import blacklist_check


class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<Text>")
    async def say(self, ctx: commands.Context, *, text):
        time = datetime.datetime.now()
        msg2 = ctx.message
        user = ctx.author.name
        if await botchannel_check(ctx):
            if await blacklist_check(self, ctx.message):
                return
            msg = await ctx.send(
                content=str(text),
                components=[
                    [
                        Button(
                            style=await get_buttoncolour(message=ctx.message),
                            label="Normal",
                            emoji="📄",
                            id="say_normal",
                            disabled=True,
                        ),
                        Button(
                            style=await get_buttoncolour(message=ctx.message),
                            label="Embed",
                            emoji="✒",
                            id="say_embed",
                        ),
                    ]
                ],
                allowed_mentions=discord.AllowedMentions.none(),
            )
            await save_message_to_cache(message=msg, author=msg2.author)
            await log(
                str(time)
                + ": Der Nutzer "
                + str(user)
                + " hat den Befehl "
                + await get_prefix_string(ctx.message)
                + "ssp benutzt!",
                guildid=ctx.guild.id,
            )

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


async def on_say_button(interaction: discord_components.interaction):
    user = interaction.author.name
    if interaction.component.id == "say_normal":
        await interaction.respond(
            type=7,
            content=interaction.message.embeds[0].description,
            embeds=[],
            components=[
                [
                    Button(
                        style=await get_buttoncolour(message=interaction.message),
                        label="Normal",
                        emoji="📄",
                        id="say_normal",
                        disabled=True,
                    ),
                    Button(
                        style=await get_buttoncolour(message=interaction.message),
                        label="Embed",
                        emoji="✒",
                        id="say_embed",
                        disabled=False,
                    ),
                ]
            ],
        )
        await log(
            f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Say-Nachricht interagiert!",
            interaction.message.guild.id,
        )

    elif interaction.component.id == "say_embed":
        embed = discord.Embed(
            title="**Say**",
            description=str(interaction.message.content),
            colour=await get_embedcolour(interaction.message),
        )
        embed._footer = await get_embed_footer(
            message=interaction.message, author=interaction.author
        )
        embed._thumbnail = await get_embed_thumbnail()
        await interaction.respond(
            type=7,
            embed=embed,
            content=" ",
            components=[
                [
                    Button(
                        style=await get_buttoncolour(message=interaction.message),
                        label="Normal",
                        emoji="📄",
                        id="say_normal",
                        disabled=False,
                    ),
                    Button(
                        style=await get_buttoncolour(message=interaction.message),
                        label="Embed",
                        emoji="✒",
                        id="say_embed",
                        disabled=True,
                    ),
                ]
            ],
        )
        await log(
            f"{datetime.datetime.now()}: Der Nutzer {user} hat mit der Say-Nachricht interagiert!",
            interaction.message.guild.id,
        )


########################################################################################################################


def setup(bot):
    bot.add_cog(say(bot))
