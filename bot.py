from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT
from forcesub import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER


    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Initialize the invitelinks dictionary
        self.invitelinks = {}

        try:
            chat_1 = await self.get_chat(FORCE_SUB_CHANNEL_1)
            link_1 = chat_1.invite_link
            if not link_1:
                await self.export_chat_invite_link(FORCE_SUB_CHANNEL_1)
                link_1 = chat_1.invite_link
            self.invitelinks[FORCE_SUB_CHANNEL_1] = link_1

            chat_2 = await self.get_chat(FORCE_SUB_CHANNEL_2)
            link_2 = chat_2.invite_link
            if not link_2:
                await self.export_chat_invite_link(FORCE_SUB_CHANNEL_2)
                link_2 = chat_2.invite_link
            self.invitelinks[FORCE_SUB_CHANNEL_2] = link_2

        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).warning("Bot encountered an issue while getting invite links!")
            self.LOGGER(__name__).warning(
                f"Bot can't Export Invite link from Force Sub Channel!")
            self.LOGGER(__name__).warning(
                f"Please Double check the FORCE_SUB_CHANNEL_ID value for and Make sure Bot is Admin in channel with Invite Users via Link Permission")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Straw_hat_piratess for support")
            sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Straw_hat_piratess for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/GeekLuffy")
        self.LOGGER(__name__).info(f""" \n\n       
                                                                                      
▀███▀▀▀███▀███▀▀▀██▄   ▄▄█▀▀▀█▄█▀███▀▀▀███    ▀███▀▀▀██▄ ▄▄█▀▀██▄ ███▀▀██▀▀███▄█▀▀▀█▄█
  ██    ▀█  ██    ▀██▄██▀     ▀█  ██    ▀█      ██    ████▀    ▀██▄▀   ██   ▀███    ▀█
  ██   █    ██     ▀███▀       ▀  ██   █        ██    ███▀      ▀██    ██    ▀███▄    
  ██████    ██      ███           ██████        ██▀▀▀█▄▄█        ██    ██      ▀█████▄
  ██   █  ▄ ██     ▄███▄    ▀████ ██   █  ▄     ██    ▀██▄      ▄██    ██    ▄     ▀██
  ██     ▄█ ██    ▄██▀██▄     ██  ██     ▄█     ██    ▄███▄    ▄██▀    ██    ██     ██
▄██████████████████▀   ▀▀███████▄██████████   ▄████████  ▀▀████▀▀    ▄████▄  █▀█████▀ 
                                                                                      
                                                                                      

                                          """)
        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")