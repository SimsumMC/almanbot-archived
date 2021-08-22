import os

from discord.ext import commands


class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def countlines(path: str):
    return len(open(path).readlines())


def deletelines(path, amount):
    with open(path, "r") as fin:
        data = fin.read().splitlines(True)
    with open(path, "w") as fout:
        fout.writelines(data[amount:])


def log(text, guildid):
    path = os.path.join("data", "logs", f"{guildid}.txt")
    with open(path, "a") as f:
        f.write("\n" + text)
    amount = countlines(path=path)
    if amount >= 199:
        deletelines(path=path, amount=amount - 200)


########################################################################################################################


def setup(bot):
    bot.add_cog(logging(bot))
