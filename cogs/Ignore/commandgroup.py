import discord
from discord.ext import commands


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="test")
    async def test(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("test 1")

    @test.group(name="firstcommand")
    async def fc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("test 2")

    @fc.command(name="secondcommand")
    async def sc(self, ctx):
        await ctx.send("test 3")

########################################################################################################################


def setup(bot):
    bot.add_cog(test(bot))