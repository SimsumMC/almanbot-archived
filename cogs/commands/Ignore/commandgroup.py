from discord.ext import commands


class commandgroup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="firstcommand", usage="<Test>")
    async def test(self, ctx, test):
        if ctx.invoked_subcommand is None:
            await ctx.send("test 1")

    @test.group(name="secondcmmand", usage="<Test>")
    async def secondcommand(self, ctx, test):
        if ctx.invoked_subcommand is None:
            await ctx.send("test 2")

    @fc.command(name="thirdcommand", usage="<Test>")
    async def thirdcommand(self, ctx, test):
        await ctx.send("test 3")

########################################################################################################################


def setup(bot):
    bot.add_cog(commandgroup(bot))
