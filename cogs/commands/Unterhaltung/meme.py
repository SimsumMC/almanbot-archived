import datetime
import json
import os
import random

import discord
import praw
from discord.ext.commands import Bot

from cogs.core.config.config_memechannel import (
    get_memechannel_obj_list,
    memechannel_check,
)
from config import (
    ICON_URL,
    THUMBNAIL_URL,
    FOOTER,
    WRONG_CHANNEL_ERROR,
    BOT_NAME,
    REDDIT_APP,
)
from discord.ext import commands

from cogs.core.functions.functions import (
    get_author,
)
from cogs.core.config.config_prefix import get_prefix_string
from cogs.core.functions.func_json import readjson
from cogs.core.config.config_memes import get_memes, redditnsfwcheck, meme_is_checked
from cogs.core.config.config_embedcolour import get_embedcolour
from cogs.core.functions.logging import log


class meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx, redditname=None):
        if redditname is None:
            redditname = get_memes(ctx.guild.id)
        global submission
        time = datetime.datetime.now()
        user = ctx.author.name
        name = ctx.channel.name
        msg2 = ctx.message
        path = os.path.join("data", "verifiedmemes", "memes.json")
        if memechannel_check(ctx):
            try:
                reddit = praw.Reddit(
                    client_id=REDDIT_APP["client_id"],
                    client_secret=REDDIT_APP["client_secret"],
                    user_agent=BOT_NAME,
                    check_for_async=False,
                )
                memes_submissions = reddit.subreddit(redditname).hot()
                post_to_pick = random.randint(1, 100)
                if (
                    redditname != get_memes(ctx.guild.id)
                    and meme_is_checked(redditname) is False
                ):
                    if redditname in readjson("failed", path) or redditnsfwcheck(
                        redditname
                    ):
                        embed = discord.Embed(
                            title="**Fehler**",
                            description=f"Der angegebene Reddit **{redditname}** enthält nicht "
                            "zulässigen Inhalt.",
                            color=get_embedcolour(ctx.message),
                        )
                        embed.set_thumbnail(url=THUMBNAIL_URL)
                        embed.set_footer(
                            text=FOOTER[0]
                            + str(user)
                            + FOOTER[1]
                            + str(get_author())
                            + FOOTER[2]
                            + str(get_prefix_string(ctx.message)),
                            icon_url=ICON_URL,
                        )
                        await ctx.send(embed=embed)
                        log(
                            f"{time}: Der Nutzer {user} hat beim Befehl"
                            f"'{get_prefix_string(ctx.message)}meme ein ungültiges Argument eingegeben.",
                            ctx.guild.id,
                        )
                        return
                    else:
                        with open(path, "r+") as f:
                            data = json.load(f)
                        data["verified"].append(redditname)
                        json.dump(data, f, indent=4)
                for i in range(0, post_to_pick):
                    submission = next(x for x in memes_submissions if not x.stickied)
                embed = discord.Embed(
                    title=f"**{submission.title}**", colour=get_embedcolour(ctx.message)
                )
                embed.set_image(url=submission.url)
                embed.set_footer(
                    text=FOOTER[0]
                    + str(user)
                    + FOOTER[1]
                    + str(get_author())
                    + FOOTER[2]
                    + str(get_prefix_string(ctx.message)),
                    icon_url=ICON_URL,
                )
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat den Befehl {get_prefix_string(ctx.message)}"
                    "meme benutzt!",
                    guildid=ctx.guild.id,
                )
                return
            except Exception:
                embed = discord.Embed(
                    title="**Fehler**",
                    description=f"Beim Reddit **{redditname}** ist wohl etwas schiefgelaufen. "
                    "Das könnte z.B. bedeuten das der Reddit nicht existiert oder das der Reddit "
                    "aufgrund von zu vielen Anfragen nicht automatisch auf NSFW Content überprüft "
                    "wurde. Sollte letzteres zutreffen, warte ein paar Minuten!",
                    color=get_embedcolour(ctx.message),
                )
                embed.set_thumbnail(url=THUMBNAIL_URL)
                embed.set_footer(
                    text=FOOTER[0]
                    + str(user)
                    + FOOTER[1]
                    + str(get_author())
                    + FOOTER[2]
                    + str(get_prefix_string(ctx.message)),
                    icon_url=ICON_URL,
                )
                await ctx.send(embed=embed)
                log(
                    f"{time}: Der Nutzer {user} hat beim Befehl"
                    f"'{get_prefix_string(ctx.message)}meme ein ungültiges Argument eingegeben.",
                    ctx.guild.id,
                )
                raise Exception

        else:
            Bot.dispatch(self.bot, "botchannelcheck_failure", ctx)


########################################################################################################################


def setup(bot):
    bot.add_cog(meme(bot))
