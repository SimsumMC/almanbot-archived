import os

import discord
from discord.ext import commands
from easy_pil import Font, Canvas, Editor, load_image_async

from cogs.core.config.config_levelling import get_user_levelling_data


class rank(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="rank")
    async def rank(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        if member.bot:
            return
        name_lenght = len(str(member))
        underline = int(name_lenght * 27) if name_lenght <= 13 else int(name_lenght * 25)
        user_data = await get_user_levelling_data(user=member, guild=ctx.guild)
        level = user_data["level"]
        xp = user_data["xp"]
        xp_for_next_level = (user_data["level"] + 1) * 100
        progress = (xp / xp_for_next_level) * 100
        background = Editor(os.path.join("data", "pictures", "rank_card.png"))
        image = await load_image_async(str(member.avatar_url))
        profile = Editor(image).resize((190, 190)).circle_image()

        poppins = Font().poppins(size=40)
        poppins_small = Font().poppins(size=30)

        background.paste(profile, (50, 50))

        background.rectangle(
            (290, 220), width=650, height=40, fill="#494b4f", radius=20
        )
        if int(progress) != 0:
            background.bar(
                (290, 220),
                max_width=650,
                height=40,
                percentage=progress,
                fill="#6FF31F",
                radius=20,
            )
        background.text((290, 40), str(member), font=poppins, color="white")

        background.rectangle((290, 100), width=underline, height=2, fill="#86EB48")
        background.text(
            (290, 125),
            f"Level : {level}\nXP : {xp} / {xp_for_next_level}",
            font=poppins_small,
            color="white",
        )

        file = discord.File(fp=background.image_bytes, filename="rank.png")
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(rank(bot))
