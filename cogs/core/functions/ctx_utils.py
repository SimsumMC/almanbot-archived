from discord.ext import commands


async def get_commandname(ctx):
    if not ctx.command:
        return ctx.message.content.split(" ")[0]
    return str(ctx.command)


class ctx_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


########################################################################################################################


def setup(bot):
    bot.add_cog(ctx_utils(bot))
