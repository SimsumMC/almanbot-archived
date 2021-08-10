from discord.ext import commands
from config import STATCORD_TOKEN
import statcord


class statcordpost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = STATCORD_TOKEN
        self.api = statcord.Client(self.bot, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(statcordpost(bot))
