import discord

OWNER_IDS = []

# BASIC THINGS

BOT_NAME = "Alman Bot"
DEFAULT_PREFIX = ["a!"]
DEFAULT_EMBEDCOLOUR = 0x41A13A
DEFAULT_BUTTONCOLOUR = "green"  # green, red, blue, grey
DEFAULT_MEMESOURCE = "memes"
ICON_URL = "https://images-ext-2.discordapp.net/external/4nupWU9g-iiaUBjdrl41CEXqLqk6uz8UJSfI24Iigmw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/802922765782089738/47e0de19ba819a95213ec35a83811c2b.webp?width=676&height=676"
THUMBNAIL_URL = "https://images-ext-2.discordapp.net/external/4nupWU9g-iiaUBjdrl41CEXqLqk6uz8UJSfI24Iigmw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/802922765782089738/47e0de19ba819a95213ec35a83811c2b.webp?width=676&height=676"
FOOTER = ["für ", " | Entwickelt von ", " | Prefix "]
STATUS = discord.Status.online
ACTIVITY_LIST = [
    "almanbot.de",
    "Einstellbaren Prefix",
    "Viele Einstellungen",
    "Open Source!",
    "in {guild_count} Servern",
    "mit {user_count} Nutzern",
    "Entwickelt von {developer_names}",
]
DEFAULT_LVLUP_MESSAGE = (
    "Herzlichen Glückwunsch, du bist auf Level {level} aufgestiegen! 🎉"
)
DEFAULT_LVLUP_MODE = "same"  # dm , channel, same
# guild_count, user_count, developer_names
DEFAULT_LEVELLING_COOLDOWN = 3
DEFAULT_LEVELLING_XP_PER_MESSAGE = 5

SUGGESTION_CHANNEL_ID = 895413425696571402

# Other Thumbnails

COIN_HEAD = "https://cdn.discordapp.com/attachments/851853486948745246/851853519497199671/kopf.png"
COIN_NUMBER = "https://cdn.discordapp.com/attachments/851853486948745246/851853652002996224/zahl.png"
SSP = "https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png"
CUBE = "https://cdn.discordapp.com/attachments/645276319311200286/803550939112931378/wurfelv2.png"
GIVEAWAY = "https://media.discordapp.net/attachments/851853486948745246/897609523911614534/1f389.png"
# TOKEN

DISCORD_TOKEN = (
    "ODEwOTMzMTI0NTk4NTk1NjE0.YCq2Uw.ZbRn0JfpKk9JN0XzRSMqgWeSVvQ"  # to run the bot
)
STATCORD_TOKEN = "statcord.com-OcSdYoeaMLzCassriL2I"  # Optional, for bot stats ->
REDDIT_APP = {  # for the memes command, just create an application on reddit
    "client_id": "JiHoJGCPBC9vlg",
    "client_secret": "egXFBVdIx7ucn9_6tji18kyLClWCIA",
}

# PATHS

CHROMEDRIVER_PATH = "C:/Users/1234n/Downloads/chromedriver_win32/chromedriver"


class lavalink:  # for music module
    host = "lava.link"
    port = "80"
    rest_uri = "http://lava.link:80"
    passwort = BOT_NAME
    identifier = BOT_NAME
    region = "europe"


# DEFAULTS | ⚠️ DANGER ZONE ⚠️ -> anything wrong here can cause crashes *while* running (when receiving messages)

DEFAULT_TRIGGER_LIST = ["Alman Bot", "SimsumMC"]
DEFAULT_TRIGGER = {
    "Alman Bot": "Hey, Ich bins!",
    "SimsumMC": "Das ist der komische RGB Fan, der für meine Existenz verantwortlich ist..."
}

""" Example for more Triggers

DEFAULT_TRIGGER_LIST = ["Alman Bot", "Käse"]
DEFAULT_TRIGGER = {
    "Alman Bot": "Hey, Ich bins!",
    "Käse": "Käse ist echt lecker LOL"
}

"""
# Messages

WRONG_CHANNEL_ERROR = (
    "Dieser Befehl kann in diesem Chat nicht genutzt werden. "
    "Hier ist eine Liste in denen der Befehl funktioniert: "
)

MISSING_PERMISSIONS_BUTTON_ERROR = (
    "Diese Nachricht gehört dir nicht! Nutz den Befehl bitte selbst!"
)

CALCULATING_ERROR = "Fehler beim berechnen!"

DEFAULT_BROADCAST_MESSAGE = "Hinweis: _Du erhälst diese Nachricht da du diesen Bot auf einem deiner Server nutzt._"

# Colour Configuration | ⚠️ DANGER ZONE ⚠️ -> anything wrong here can cause crashes *while* running (at any action)

EMBEDCOLOUR_CODES = {
    "rot": 0xA80000,
    "hellrot": 0xF00000,
    "gelb": 0xF3D720,
    "hellblau": 0x2FA5EE,
    "blau": 0x573CE2,
    "hellgrün": 0x20DE12,
    "grün": 0x41A13A,
    "hellorange": 0xE29455,
    "orange": 0xE36D0D,
    "schwarz": 0x000000,
    "hellgrau": 0x999494,
    "grau": 0x444141,
    "weiß": 0xFFFFFF,
    "dunkellila": 0x852598,
    "lila": 0xB144E4,
    "pink": 0xE114BC,
    "random": "random",
    "rainbow": "rainbow",
}

EMBEDCOLOURS_SUPPORTED = [
    "rot",
    "hellrot",
    "hellblau",
    "blau",
    "hellgrün",
    "grün",
    "hellorange",
    "orange",
    "schwarz",
    "hellgrau",
    "grau",
    "weiß",
    "dunkellila",
    "lila",
    "pink",
    "rainbow",
    "random",
    "gelb",
]

# Developer Settings | ⚠️ DANGER ZONE ⚠️ -> anything wrong here can cause the bot to instant leave your server and misfunctions

TESTING_MODE = False # only allowing Servers to join GUILDS with ID in TESTING_GUILDS, removes guild owner bypasses and more
TESTING_GUILDS = [802923248840867840, 778288526608433172, 825502579474563103]

WRONG_CHANNEL_ERROR_DELETE_AFTER = 5
BLACKLIST_DELETE_AFTER = 5

BLACKLIST_IGNORE = ["blacklist", "qr", "broadcast"]

# © github.com/SimsumMC | You're not allowed to change the following parts without my (github.com/SimsumMC) permission ⚠️

BOT_MAIN_DEVELOPER = "SimsumMC#2248"
BOT_DEVELOPERLIST = ["SimsumMC#2248"]
INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=802922765782089738&permissions=2620914775&redirect_uri=https%3A%2F%2Fdiscord.events.stdlib.com%2Fdiscord%2Fauth%2F&scope=bot%20applications.commands"
DISCORD_LINK = "https://discord.almanbot.de"
WEBSITE_LINK = "https://almanbot.de/"
GITHUB_LINK = "https://github.com/SimsumMC/almanbot/"
TOPGG_LINK = "https://top.gg/bot/802922765782089738"
ABOUT = f"""
Egal ob Moderation, einfach ein Lächeln aufs Gesicht zaubern, eine Matheaufgabe lösen oder den Avatar von einem Nutzer 
klauen - ich helfe dir wo ich nur kann! Penibel wie ein Deutscher bin ich natürlich auch...
        """

BANNER = """
     **      **                                    ******              **    
    ****    /**                                   /*////**            /**    
   **//**   /** **********   ******   *******     /*   /**   ******  ******  
  **  //**  /**//**//**//** //////** //**///**    /******   **////**///**/   
 ********** /** /** /** /**  *******  /**  /**    /*//// **/**   /**  /**    
/**//////** /** /** /** /** **////**  /**  /**    /*    /**/**   /**  /**    
/**     /** *** *** /** /**//******** ***  /**    /******* //******   //**   
//      // /// ///  //  //  //////// ///   //     ///////   //////     //    
        """
