import discord

# BASIC THINGS

BOT_NAME = "Alman Bot"
DEFAULT_PREFIX = "a!"
DEFAULT_EMBEDCOLOUR = 0x41A13A
DEFAULT_BUTTONCOLOUR = "green"  # green, red, blue, grey
DEFAULT_MEMESOURCE = "memes"
ICON_URL = "https://images-ext-2.discordapp.net/external/4nupWU9g-iiaUBjdrl41CEXqLqk6uz8UJSfI24Iigmw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/802922765782089738/47e0de19ba819a95213ec35a83811c2b.webp?width=676&height=676"
THUMBNAIL_URL = "https://images-ext-2.discordapp.net/external/4nupWU9g-iiaUBjdrl41CEXqLqk6uz8UJSfI24Iigmw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/802922765782089738/47e0de19ba819a95213ec35a83811c2b.webp?width=676&height=676"
FOOTER = ["für ", " | Entwickelt von ", " | Prefix "]
STATUS = discord.Status.online
ACTIVITY_LIST = [
    "discord.visitlink.de",
    "Einstellbaren Prefix",
    "Viele Einstellungen",
    "Open Source!",
    "in {guild_count} Servern",
    "mit {user_count} Nutzern",
    "Entwickelt von {developer_names}",
]  # guild_count, user_count, developer_names

# Other Thumbnails

COIN_HEAD = "https://cdn.discordapp.com/attachments/851853486948745246/851853519497199671/kopf.png"
COIN_NUMBER = "https://cdn.discordapp.com/attachments/851853486948745246/851853652002996224/zahl.png"
SSP = "https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png"
CUBE = "https://cdn.discordapp.com/attachments/645276319311200286/803550939112931378/wurfelv2.png"

# TOKEN

DISCORD_TOKEN = "token"  # to run the bot
STATCORD_TOKEN = "token"  # Optional, for bot stats
REDDIT_APP = {  # for the memes command, just create an application on reddit
    "client_id": "client_id",
    "client_secret": "secret"
}

# DEFAULT TRIGGER | ⚠️ DANGER ZONE ⚠️ -> anything wrong here can cause crashes *while* running (when receiving messages)

DEFAULT_TRIGGER_LIST = ["Alman Bot"]
DEFAULT_TRIGGER = {
    "Alman Bot": "Hey, Ich bins!",
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
        "bunt",
        "rainbow",
        "random",
        "gelb",
    ]

# © github.com/SimsumMC | You're not allowed to change the following parts without my (github.com/SimsumMC) permission ⚠️

BOT_MAIN_DEVELOPER = "SimsumMC#0001"
BOT_DEVELOPERLIST = ["SimsumMC#0001"]
INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=802922765782089738&scope=bot&permissions=2620914775"
DISCORD_LINK = "https://discord.visitlink.de"
WEBSITE_LINK = "https://communitybot.visitlink.de/"
GITHUB_LINK = "https://github.com/SimsumMC/almanbot/"

ABOUT = f"""
Egal ob Moderation, einfach ein bisschen Spaß haben oder den Avatar von einem Nutzer klauen - ich helfe dir wo ich nur kann!
Penibel wie ein echter Alman bin ich natürlich auch...
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
