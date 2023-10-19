# (©)@EdgeBots

import os
import asyncio
import sys

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, OWNER_ID, MAIN_CHANNEL
from forcesub import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2

from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⚡ 𝙹𝚘𝚒𝚗 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 ⚡', url=f'https://t.me/AnimeX_Horizon')
        ],
        [
            InlineKeyboardButton('⛩ 𝙰𝚋𝚘𝚞𝚝', 'about'),
            InlineKeyboardButton('🔐 𝙲𝚕𝚘𝚜𝚎', 'close')
        ]
    ]
)
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return


# =====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""


# =====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Bot, message: Message):
    buttons = []

    # If the user has not joined both channels, display the join buttons
    if FORCE_SUB_CHANNEL_1 in client.invitelinks and FORCE_SUB_CHANNEL_2 in client.invitelinks:
        buttons.append([
            InlineKeyboardButton(
                text="⚡️ Join Channel 1 ⚡️",
                url=client.invitelinks[FORCE_SUB_CHANNEL_1]
            ),
            InlineKeyboardButton(
                text="⚡️ Join Channel 2 ⚡️",
                url=client.invitelinks[FORCE_SUB_CHANNEL_2]
            )
        ])

    try:
        buttons.append([
            InlineKeyboardButton(
                text='Try Again',
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass

    markup = InlineKeyboardMarkup(buttons)

    await message.reply_text(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=markup,
        quote=True,
        disable_web_page_preview=True
    )


# Command callback for changing force subscribe channels
@Bot.on_message(filters.command('setchannels') & filters.private & filters.user(ADMINS))
async def set_channels(client: Bot, message: Message):
    if len(message.command) == 3:
        new_channel_id_1 = int(message.command[1])
        new_channel_id_2 = int(message.command[2])

        # Update the global variables
        global FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2
        FORCE_SUB_CHANNEL_1 = new_channel_id_1
        FORCE_SUB_CHANNEL_2 = new_channel_id_2

        # Update the config variables in your_config_file.py
        with open("forcesub.py", "w") as config_file:
            config_file.write(f"FORCE_SUB_CHANNEL_1 = {FORCE_SUB_CHANNEL_1}\n")
            config_file.write(f"FORCE_SUB_CHANNEL_2 = {FORCE_SUB_CHANNEL_2}\n")

        await message.reply_text(f"Force subscribe channels updated to {new_channel_id_1} and {new_channel_id_2}")
    else:
        await message.reply_text("Please provide two valid channel IDs after command.\nEx: /setchannels -100123456789 -100987654321")


# Command callback for checking current force subscribe channels
@Bot.on_message(filters.command('checkchannels') & filters.private & filters.user(ADMINS))
async def check_channels(client: Bot, message: Message):
    channel_info = []

    for channel_id in [FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2]:
        try:
            chat = await client.get_chat(channel_id)
            channel_name = chat.title
            channel_info.append(f"<b>🫧 {channel_name} ({channel_id})</b>")
        except Exception as e:
            channel_info.append(f"<b>🫧 Unknown Channel ({channel_id})</b>")

    channels_text = "\n".join(channel_info)
    await message.reply_text(f"<u><b>Current Force Subscribe Channels:</b></u>\n\n{channels_text}")

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"Currently {len(users)} users are using this bot")

# Restart to cancel all processes
@Bot.on_message(filters.private & filters.command("restart") & filters.user(ADMINS))
async def restart_bot(b, m):
    restarting_message = await m.reply_text(f"⚡️<b><i>Restarting....</i></b>", disable_notification=True)

    # Wait for 3 seconds
    await asyncio.sleep(3)

    # Update message after the delay
    await restarting_message.edit_text("✅ <b><i>Successfully Restarted</i></b>")

    # Restart the bot
    os.execl(sys.executable, sys.executable, *sys.argv)

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
