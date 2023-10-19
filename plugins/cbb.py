#(©)@EdgeBots

from pyrogram import __version__

import config
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"""<b>╭───────────⍟
├➽ Dᴇᴠᴇʟᴏᴩᴇʀ : <a href='tg://user?id={OWNER_ID}'>Nigga</a>
├➽ Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pʏʀᴏɢʀᴀᴍ</a>
├➽ Lᴀɴɢᴜᴀɢᴇ : <a href=https://www.python.org>Pʏᴛʜᴏɴ 3</a>
├➽ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ : <a href=https://t.me/kanaoXhizuru>Source</a>
├➽ Mᴀɪɴ Cʜᴀɴɴᴇʟ : <a href=https://t.me/AnimeX_Horizon>Aɴɪᴍᴇ Eᴅɢᴇ</a>
├➽ Mᴀɪɴ Gʀᴏᴜᴘ : <a href=https://t.me/Scout_Legion>Sᴛʀᴀᴡʜᴀᴛ Pɪʀᴀᴛᴇꜱ</a></b>
╰───────────────⍟ """,
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝙲𝚕𝚘𝚜𝚎", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
