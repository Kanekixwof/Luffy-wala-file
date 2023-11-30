#(©)@EdgeBots

import os
import logging
from logging.handlers import RotatingFileHandler

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6613285947:AAEV_8_bMS_zbTSgkG8207QMfy4CMPAKYrk")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID","19406037"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "aa8cac013b63982efea11d1370b0151c")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001797213646"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5910975386"))
MAIN_CHANNEL = (os.environ.get("OWNER_ID", "5348193047"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://public:abishnoimf@cluster0.rqk6ihd.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "edgefilebot")

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI'm here to help! I keep private files in a special channel and share links so others can access them effortlessly.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "6210050767 5910975386 6367644526").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", """<b>Hold on, {mention}!\n
You're missing out on some serious action.\n
To unleash my full power and access all the files, you've got to join both of our electrifying channels below:</b>""")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "🚫 Please avoid direct messages. I'm here solely for file sharing!"

ADMINS.append(OWNER_ID)
ADMINS.append(5348193047)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
