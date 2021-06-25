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
        if not data["trigger"]:
            data["trigger"] = []
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            return data["trigger"]
        return data["trigger"]
    except Exception:
        print(Exception)
        return []


def get_trigger_msg(guildid, trigger):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
        msg = data["triggermsg"][trigger]
        return msg
    except Exception:
        print(Exception)
        return None


def add_trigger(guildid, trigger, msg):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
            f.close()
        data["trigger"].append(trigger)
        data["triggermsg"][trigger] = msg
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        print(Exception)
        return False


def remove_trigger(guildid, trigger):
    try:
        path = os.path.join("data", "configs", f"{guildid}.json")
        with open(path, "r") as f:
            data = json.load(f)
            f.close()
        data["trigger"].remove(trigger)
        del data["triggermsg"][trigger]
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        print(Exception)
        return False


########################################################################################################################


def setup(bot):
    bot.add_cog(trigger_func(bot))
