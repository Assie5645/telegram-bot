from telethon import TelegramClient, events
import json
import os

# ==========================
# 🔑 API CREDENTIALS
# ==========================
api_id = 30133788
api_hash = "1f2d2d024eaafe22909fbb1131e1f084"

# ==========================
# 📡 SOURCE CHANNELS
# ==========================
source_channels = [
    "@AAUMEREJA",
    "@AAU_GENERAL",
    "@PECCAAiT",
    "@AAUNews11"
]

# ==========================
# 🎯 DESTINATION CHANNEL
# ==========================
destination_channel = "@AAUCentral"

# ✅ IMPORTANT — Use NEW session name
client = TelegramClient("new_session", api_id, api_hash)

DATA_FILE = "processed.json"

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            processed_ids = json.load(f)
    except:
        processed_ids = {}
else:
    processed_ids = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(processed_ids, f)


print("🚀 BOT STARTED — PROFESSIONAL MODE")


@client.on(events.Album(chats=source_channels))
async def handle_album(event):

    album_id = str(event.grouped_id)

    if album_id in processed_ids:
        try:
            old_msg_id = processed_ids[album_id]
            await client.delete_messages(destination_channel, old_msg_id)
        except:
            pass

    files = [msg.media for msg in event.messages]
    caption = event.messages[0].text or ""

    sent = await client.send_file(
        destination_channel,
        files,
        caption=caption
    )

    processed_ids[album_id] = sent.id
    save_data()

    print("📸 Album forwarded")


@client.on(events.NewMessage(chats=source_channels))
async def handle_message(event):

    message = event.message

    if message.grouped_id:
        return

    unique_key = f"{message.chat_id}_{message.id}"

    if unique_key in processed_ids:
        try:
            old_msg_id = processed_ids[unique_key]
            await client.delete_messages(destination_channel, old_msg_id)
        except:
            pass

    text = message.text or ""

    if message.media:
        sent = await client.send_file(
            destination_channel,
            message.media,
            caption=text
        )
    else:
        sent = await client.send_message(
            destination_channel,
            text
        )

    processed_ids[unique_key] = sent.id
    save_data()

    print("✅ Message forwarded")


client.start()
client.run_until_disconnected()
