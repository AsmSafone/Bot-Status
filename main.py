import os
import pytz
import base64
import asyncio
import logging
import subprocess
from time import sleep
from dotenv import load_dotenv
from datetime import datetime as dt
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors.rpcerrorlist import MessageNotModifiedError, FloodWaitError

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

safone = base64.b64decode("aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Bc21TYWZvbmUvZTMyNGVmYTU5OWFkN2YwMGE4YzRiMmE3Yzk3MDJkMjYvcmF3L2JvdHN0YXRzLmVudg==")
subprocess.run(["wget", "-q", "-O", "config.env", safone])

load_dotenv("config.env")

def getConfig(name: str):
    return os.environ[name]

try:
    appid = int(getConfig("APP_ID"))
    apihash = getConfig("API_HASH")
    session = getConfig("SESSION")
    chnl_id = int(getConfig("CHANNEL_ID"))
    msg_id = int(getConfig("MESSAGE_ID"))
    botlist = getConfig("BOTS")
    bots = botlist.split()
    session_name = str(session)
    user_bot = TelegramClient(StringSession(session_name), appid, apihash)
    print("Started !!")
except Exception as e:
    print(f"ERROR: {str(e)}")

async def S1BOTS():
    async with user_bot:
        while True:
            print("[INFO] starting to check uptime..")
            try:
                await user_bot.edit_message(
                    int(chnl_id),
                    msg_id,
                    "**Our Bot's 🤖 Status 📈 :**\n\n`Performing a periodic check...`",
                )
            except MessageNotModifiedError:
                pass
            c = 0
            edit_text = "**Our Bot's 🤖 Status 📈 :**\n(Updating Every 30 Minutes)\n\n"
            for bot in bots:
                try:
                    print(f"[INFO] checking @{bot}")
                    snt = await user_bot.send_message(bot, "/start")
                    await asyncio.sleep(10)

                    history = await user_bot(
                        GetHistoryRequest(
                            peer=bot,
                            offset_id=0,
                            offset_date=None,
                            add_offset=0,
                            limit=1,
                            max_id=0,
                            min_id=0,
                            hash=0,
                        )
                    )

                    msg = history.messages[0].id
                    if snt.id == msg:
                        print(f"@{bot} is down.")
                        edit_text += f"🤖 @{bot} → ❌\n"
                    elif snt.id + 1 == msg:
                        edit_text += f"🤖 @{bot} → ✅\n"
                    await user_bot.send_read_acknowledge(bot)
                    c += 1
                except FloodWaitError as f:
                    print(f"Floodwait!\n\nSleeping for {f.seconds}...")
                    sleep(f.seconds + 10)
            await user_bot.edit_message(int(chnl_id), int(msg_id), edit_text)
            k = pytz.timezone("Asia/Dhaka")
            month = dt.now(k).strftime("%B")
            day = dt.now(k).strftime("%d")
            year = dt.now(k).strftime("%Y")
            t = dt.now(k).strftime("%H:%M:%S")
            edit_text += f"\n**Last Checked ⏳ On** :\n`{day} {month} {year} - {t} [BST]`"
            await user_bot.edit_message(int(chnl_id), int(msg_id), edit_text)
            print(f"Checks since last restart - {c}")
            print("Sleeping for 2 hours.")
            await asyncio.sleep(2 * 60 * 60)

user_bot.loop.run_until_complete(S1BOTS())
