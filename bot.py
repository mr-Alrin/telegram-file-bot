from pyrogram import Client, filters
from pymongo import MongoClient
import os

# Load environment variables correctly
BOT_TOKEN = os.environ.get("7743489209:AAEwyaWftk_9WiYWM6exT7sjLxJLc4X-Tf0")
API_ID = int(os.environ.get("34411805"))
API_HASH = os.environ.get("f10c95e5c2af623eaf9fa81dd6695e59")
DB_URI = os.environ.get("mongodb+srv://alrin01:anubhav%40123@cluster0.0l1f6oi.mongodb.net/?appName=Cluster0")

# Initialize bot
bot = Client("FileStoreBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Connect MongoDB
mongo_client = MongoClient(DB_URI)
db = mongo_client["filebot"]
users_col = db["users"]

# --- Handlers ---

@bot.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # Save user in database if not exists
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "first_name": first_name})
        message.reply_text(f"👋 Hello {first_name}! You are now registered in the database.")
    else:
        message.reply_text(f"Welcome back to our bot Crynchy Filestore bot {first_name}! 👋")

@bot.on_message(filters.document | filters.video | filters.photo)
def file_handler(client, message):
    file_id = None
    file_type = None

    if message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.video:
        file_id = message.video.file_id
        file_type = "video"
    elif message.photo:
        file_id = message.photo.file_id
        file_type = "photo"

    if file_id:
        db.files.insert_one({
            "user_id": message.from_user.id,
            "file_id": file_id,
            "file_type": file_type
        })
        message.reply_text("✅ File saved successfully!")

print("✅ Bot is running...")
bot.run()
