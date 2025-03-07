import os
import pytz
import asyncio
import logging
from dotenv import load_dotenv
from datetime import datetime as dt
from telethon import TelegramClient, utils
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors.rpcerrorlist import MessageNotModifiedError, FloodWaitError

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)
load_dotenv()


async def S1BOTS():
    def getConfig(name: str):
        return os.environ[name]
    try:
        bots = getConfig("BOTS").split()
        user_bot = TelegramClient(
            StringSession(getConfig("SESSION")),
            int(getConfig("APP_ID")),
            getConfig("API_HASH"),
        )
        user_bot.parse_mode = "markdown"
    except Exception as e:
        logging.error(f"ERROR: {str(e)}")
        return

    async with user_bot:
        while True:
            print("[INFO] Starting client...")
            try:
                await user_bot.edit_message(
                    int(getConfig("CHANNEL_ID")),
                    int(getConfig("MESSAGE_ID")),
                    "**Our Bot's 🤖 Status 📈 :**\n\n`Performing a periodic check...`",
                )
            except MessageNotModifiedError:
                pass
            c = 0
            edit_text = "**Our Bot's 🤖 Status 📈 :**\n(Updating Every 30 Minutes)\n\n"
            print("[INFO] Starting to check uptime...")
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
                        print(f"[WARNING] @{bot} is down.")
                        full_user = await user_bot.get_entity(bot)
                        edit_text += f"➧ **[{utils.get_display_name(full_user)}](https://t.me/{bot})** [⚰️]\n"
                    elif snt.id + 1 == msg:
                        full_user = await user_bot.get_entity(bot)
                        edit_text += f"➧ **[{utils.get_display_name(full_user)}](https://t.me/{bot})** [⚡️]\n"
                    c += 1
                    await user_bot.send_read_acknowledge(bot)
                    await user_bot.edit_message(int(getConfig("CHANNEL_ID")), int(getConfig("MESSAGE_ID")), edit_text)
                except MessageNotModifiedError:
                    print(f"[WARNING] Unable to edit message...")
                    pass
                except FloodWaitError as f:
                    print(f"[WARNING] Floodwait, Sleeping for {f.seconds}...")
                    await asyncio.sleep(f.seconds + 10)
            print(f"[INFO] Checks since last restart - {c}")
            k = pytz.timezone("Asia/Dhaka")
            month = dt.now(k).strftime("%B")
            day = dt.now(k).strftime("%d")
            year = dt.now(k).strftime("%Y")
            t = dt.now(k).strftime("%H:%M:%S")
            edit_text += f"\n**Last Checked ⏳ On** :\n`{day} {month} {year} - {t} [BST]`"
            await user_bot.edit_message(int(getConfig("CHANNEL_ID")), int(getConfig("MESSAGE_ID")), edit_text)
            print("[INFO] Check done, Sleeping for 2 hours...")
            await asyncio.sleep(2 * 60 * 60)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(S1BOTS())
