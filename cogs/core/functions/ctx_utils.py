from discord.ext import commands


async def get_commandname(ctx):
    if not ctx.command:
        return ctx.message.content.split(" ")[0]
    elif ctx.invoked_subcommand:
        parents = ""
        for p in ctx.invoked_parents:
            parents = parents + p + " "
        parents = parents[:-1]
        commandname = str(parents) + " " + str(ctx.invoked_subcommand.name)
    else:
        commandname = ctx.command.name
    return commandname


class ctx_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


########################################################################################################################


def setup(bot):
    bot.add_cog(ctx_utils(bot))
