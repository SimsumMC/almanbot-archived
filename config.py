import discord

# BASIC THINGS

BOT_NAME = "Alman Bot"
DEFAULT_PREFIX = "a!"
DEFAULT_COLOUR = 0x41A13A
DEFAULT_MEMESOURCE = "memes"
ICON_URL = "https://images-ext-2.discordapp.net/external/4nupWU9g-iiaUBjdrl41CEXqLqk6uz8UJSfI24Iigmw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/802922765782089738/47e0de19ba819a95213ec35a83811c2b.webp?width=676&height=676"
THUMBNAIL_URL = "https://images-ext-2.discordapp.net/external/4nupWU9g-iiaUBjdrl41CEXqLqk6uz8UJSfI24Iigmw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/802922765782089738/47e0de19ba819a95213ec35a83811c2b.webp?width=676&height=676"
FOOTER = ["für ", " | Entwickelt von ", " | Prefix "]
STATUS = discord.Status.online
STATUS_LIST = [
    "discord.visitlink.de",
    "Einstellbaren Prefix!",
    "Viele Einstellungen!",
    "Open Source!",
    "in {guild_count} Servern!",
    "Entwickelt von {developer_names}",
]  # guild_count, player_count, developer_names

# Other Thumbnails

COIN_HEAD = "https://cdn.discordapp.com/attachments/851853486948745246/851853519497199671/kopf.png"
COIN_NUMBER = "https://cdn.discordapp.com/attachments/851853486948745246/851853652002996224/zahl.png"
SPP = "https://cdn.discordapp.com/attachments/645276319311200286/803373963316953158/stp.png"
CUBE = "https://cdn.discordapp.com/attachments/645276319311200286/803550939112931378/wurfelv2.png"

# TOKEN

DISCORD_TOKEN = "token" # to run the bot
STATCORD_TOKEN = "token"  # Optional
REDDIT_APP = {  # for the memes command
    "client_id": "id",
    "client_secret": "token"
}

# DEFAULT TRIGGER

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
    "Dieser Befehl kann in diesem Kanal nicht genutzt werden. "
    "Hier ist eine Liste in denen der Befehl funktioniert: "
)

# © github.com/SimsumMC | You're not allowed to change the following parts ⚠️

BOT_MAIN_DEVELOPER = "SimsumMC#0001"
BOT_DEVELOPERLIST = ["SimsumMC#0001"]
INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=802922765782089738&scope=bot&permissions=2620914775"
DISCORD_LINK = "https://discord.visitlink.de"
WEBSITE_LINK = "https://communitybot.visitlink.de/"
GITHUB_LINK = "https://github.com/SimsumMC/communitybot/"
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
