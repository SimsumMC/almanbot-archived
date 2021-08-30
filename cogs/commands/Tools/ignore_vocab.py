import os

from discord.ext import commands
import discord


class vocab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="vocab", aliases="vokabeln")
    async def vocab(self, ctx):
        pass

    @vocab.command()
    async def add(self, ctx, name, *, vocabs):
        path = os.path.join("")

    @vocab.command()
    async def remove(self, ctx, name):
        pass

    @vocab.command()
    async def list(self, ctx, name):
        pass

    @vocab.command()
    async def quiz(self, ctx, name):
        pass


########################################################################################################################


def setup(bot):
    bot.add_cog(vocab(bot))
