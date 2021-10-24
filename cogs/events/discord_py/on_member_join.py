import discord
from discord.ext import commands

from cogs.core.config.config_autoroles import get_autoroles
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.defaults.defaults_embed import get_embed_footer, get_embed_thumbnail


class on_member_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member):

        # autoroles

        roles = await get_autoroles(member.guild)
        for role in roles:
            try:
                await member.add_roles(role)
            except Exception:
                embed = discord.Embed(
                    title="Fehler",
                    description=f"Dem Nutzer {str(member)} konnte folgende Autorole nicht gegeben werden: {role.name}!",
                    colour=await get_embedcolour(guild=member.guild),
                )
                embed._footer, embed._thumbnail = (
                    await get_embed_footer(
                        guild=member.guild, author=member.guild.owner
                    ),
                    await get_embed_thumbnail(),
                )
                await member.guild.owner.send(embed=embed)

        # join message


########################################################################################################################


def setup(bot):
    bot.add_cog(on_member_join(bot))
