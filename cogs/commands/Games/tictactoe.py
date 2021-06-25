import asyncio
import datetime
import json

import discord
import random
import os
from discord.ext import commands

from cogs.core.functions.functions import get_botc, get_author, get_prefix_string, get_colour, readjson, writejson
from cogs.core.functions.functions import log

konditionen = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class tictactoe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tictactoe(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('info about tictactoe should be here')

    @tictactoe.command()
    async def start(self, ctx, spieler1: discord.Member, spieler2: discord.Member):
        print("start")
        if create_game(ctx.guild.id, spieler1.id, spieler2.id) is False:
            await ctx.send(f"game started, use tictactoe setze zum spielen: Am zug ist {spieler2.mention}")
            return
        await ctx.send("game already exist")

    @tictactoe.command()
    async def setze(self, ctx, number):
        possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        gameid = get_gameid(ctx.guild.id, ctx.author.id)
        if number in possible:
            pass
        else:
            await ctx.send("invalid")
            return
        if get_turn(ctx.guild.id, gameid) == ctx.author.id:
            pass
        else:
            await ctx.send("Du bist nicht am Zug!")
        get_embed()

    @tictactoe.command()
    async def stop(self, ctx):
        gameid = get_gameid(ctx.guild.id, ctx.author.id)
        if delete_game(ctx.guild.id, gameid):
            await ctx.send("game deleted")


def create_game(guildid, player1, player2):
    path = os.path.join('data', 'games', 'tictactoe', f'{guildid}.json')
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            data = {"gamemax": 0, "active": [], "player": {}, "data": {}}
            json.dump(data, f, indent=4)
    if readjson("player"[player1], path):
        return False
    elif readjson("player"[player2], path):
        return False
    else:
        with open(path, 'r') as f:
            data = json.load(f)
        id = data["gamemax"] + 1
        data["active"].append(id)
        data["player"[player1]] = id
        data["player"[player2]] = id
        data["data"[id]] = {"player": [player1, player2],
                            "turn": player2,
                            "kreuz": player1,
                            "kreis": player2,
                            player1: [],
                            player2: []}
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        print(data)
        return True


def get_gameid(guildid, player):
    path = os.path.join('data', 'games', 'tictactoe', f'{guildid}.json')
    with open(path, 'r') as f:
        data = json.load(f)
        print(data)
        return True and data["player"[player]]


def get_turn(guildid, gameid):
    path = os.path.join('data', 'games', 'tictactoe', f'{guildid}.json')
    with open(path, 'r') as f:
        data = json.load(f)
        print(data)
        return True and data["data"[gameid["turn"]]]


def check_win(guildid, gameid, player):
    path = os.path.join('data', 'games', 'tictactoe', f'{guildid}.json')
    with open(path, 'r') as f:
        data = json.load(f)
        print(data)
    if tictactoe_check(data["data"[gameid[player]]]):
        return True
    return False


def tictactoe_check(liste):
    global konditionen
    for kondition in konditionen:
        if kondition in liste:
            return True
    return False


def get_embed(guildid, gameid, player, turn):
    path = os.path.join('data', 'games', 'tictactoe', f'{guildid}.json')
    with open(path, 'r+') as f:
        data = json.load(f)
    playerlist = data[["data"[gameid["player"]]]]
    if player == playerlist[1]:
        number = 1
    elif player == playerlist[2]:
        number = 2


def delete_game(guildid, gameid):
    try:
        path = os.path.join('data', 'games', 'tictactoe', f'{guildid}.json')
        with open(path, 'r') as f:
            data = json.load(f)
            print(data)
        # remove game from active
        data["active"].remove(gameid)
        # remove player id definings
        player = data["data"[gameid["player"]]]
        del player[1]
        del player[2]
        # delete game data
        del data["data"[gameid]]
        print(data)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        raise Exception
        return False


########################################################################################################################


def setup(bot):
    bot.add_cog(tictactoe(bot))
