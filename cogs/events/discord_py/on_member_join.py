from discord.ext import commands

from cogs.core.config.config_autoroles import get_autoroles


class on_member_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member):
        # autoroles
        roles = await get_autoroles(member.guild)
        print(roles)
        for role in roles:
            try:
                await member.add_roles(role)
            except Exception:
                await member.guild.owner.send("Error")  # Message that its not possible to add this role


########################################################################################################################


def setup(bot):
    bot.add_cog(on_member_join(bot))
