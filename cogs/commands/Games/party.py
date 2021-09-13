import discord
from discord.ext import commands


async def get_game_invite(ctx: commands.Context, game):
    print(-1)
    application_ids = {
        "youtube": 755600276941176913,
        "poker": 755827207812677713,
        "betrayal": 773336526917861400,
        "fishing": 814288819477020702,
        "schach": 832012774040141894,
    }
    print(0)
    gameid = application_ids.get(game)
    print(1)
    data = await ctx.author.voice.channel.guild.state.http.create_invite(
        ctx.author.voice.channel.id,
        reason=None,
        max_age=0,
        max_uses=0,
        temporary=False,
        unique=True,
        target_type=3,
        target_user_id=None,
        target_application_id=gameid,
    )
    print(2)
    print(data)
    return data


class party(commands.Cog):
    def __innit__(self, bot):
        self.bot = bot

    @commands.command(
        name="party",
        aliases=["together", "watchtogether"],
        usage="<YouTube / Poker / Betrayal / Fishing / Schach>",
    )
    async def party(self, ctx, game):
        print("party-1")
        games = ["youtube", "poker", "betrayal", "fishing", "schach"]
        if game.lower() not in games:
            # todo error handling
            return
        elif not ctx.author.voice:
            # todo error handling
            return
        gamelink = await get_game_invite(ctx, game.lower)
        print(gamelink)
        await ctx.send(gamelink)


########################################################################################################################


def setup(bot):
    bot.add_cog(party(bot))
