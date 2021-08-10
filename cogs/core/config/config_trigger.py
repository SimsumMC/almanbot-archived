import json
import os

from discord.ext import commands


class trigger_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def get_trigger_list(guildid):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
        if not data["trigger"]["triggerlist"]:
            data["trigger"]["triggerlist"] = []
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            return data["triggerlist"]
        return data["trigger"]["triggerlist"]
    except Exception:
        raise Exception


def get_trigger_msg(guildid, trigger):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
        msg = data["trigger"]["triggermsg"][trigger]
        if not msg:
            return "Unbekannter Fehler! Specification: 'trigger-get-msg-unknown'"
        return msg
    except Exception:
        raise Exception


def add_trigger(guildid, trigger, msg):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
            f.close()
        if not data["trigger"]["triggerlist"]:
            data["trigger"]["triggerlist"] = []
        data["trigger"]["triggerlist"].append(trigger)
        if not data["trigger"]["triggermsg"]:
            data["trigger"]["triggermsg"] = {}
        data["trigger"]["triggermsg"][trigger] = msg
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        raise Exception


def remove_trigger(guildid, trigger):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
            f.close()
        data["trigger"]["triggerlist"].remove(trigger)
        del data["trigger"]["triggermsg"][trigger]
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        raise Exception


########################################################################################################################


def setup(bot):
    bot.add_cog(trigger_func(bot))
