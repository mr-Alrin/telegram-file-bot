import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token - BotFather se milega
BOT_TOKEN = "7743489209:AAEwyaWftk_9WiYWM6exT7sjLxJLc4X-Tf0"

# File ID storage dictionary
file_storage = {}
file_counter = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    await update.message.reply_text(
        "🗂️ *File Storage Bot*\n\n"
        "Commands:\n"
        "/start - Bot start karo\n"
        "/help - Help dekho\n"
        "/list - Saved files dekho\n"
        "/get <id> - File download karo\n\n"
        "Koi bhi file bhejo, main store kar lunga!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📚 *Kaise Use Karein:*\n\n"
        "1️⃣ Koi bhi file, photo, video, document bhejo\n"
        "2️⃣ Bot tumhe ek unique ID dega\n"
        "3️⃣ `/get <id>` se file wapas pao\n"
        "4️⃣ `/list` se sab files dekho",
        parse_mode='Markdown'
    )

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all stored files"""
    if not file_storage:
        await update.message.reply_text("❌ Koi file stored nahi hai abhi tak!")
        return
    
    message = "📁 *Stored Files:*\n\n"
    for file_id, file_info in file_storage.items():
        message += f"ID: `{file_id}` - {file_info['name']}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Retrieve a file by ID"""
    if not context.args:
        await update.message.reply_text("❌ File ID chahiye!\nExample: `/get 1`", parse_mode='Markdown')
        return
    
    file_id = context.args[0]
    
    if file_id not in file_storage:
        await update.message.reply_text("❌ Ye ID exist nahi karta!")
        return
    
    file_info = file_storage[file_id]
    
    try:
        if file_info['type'] == 'document':
            await update.message.reply_document(file_info['telegram_id'])
        elif file_info['type'] == 'photo':
            await update.message.reply_photo(file_info['telegram_id'])
        elif file_info['type'] == 'video':
            await update.message.reply_video(file_info['telegram_id'])
        elif file_info['type'] == 'audio':
            await update.message.reply_audio(file_info['telegram_id'])
        elif file_info['type'] == 'voice':
            await update.message.reply_voice(file_info['telegram_id'])
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store document files"""
    global file_counter
    file_counter += 1
    
    file_id = str(file_counter)
    telegram_file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    
    file_storage[file_id] = {
        'telegram_id': telegram_file_id,
        'name': file_name,
        'type': 'document'
    }
    
    await update.message.reply_text(
        f"✅ Document saved!\n"
        f"📄 Name: `{file_name}`\n"
        f"🆔 ID: `{file_id}`\n\n"
        f"Retrieve: `/get {file_id}`",
        parse_mode='Markdown'
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store photos"""
    global file_counter
    file_counter += 1
    
    file_id = str(file_counter)
    telegram_file_id = update.message.photo[-1].file_id
    
    file_storage[file_id] = {
        'telegram_id': telegram_file_id,
        'name': f'photo_{file_id}.jpg',
        'type': 'photo'
    }
    
    await update.message.reply_text(
        f"✅ Photo saved!\n"
        f"🆔 ID: `{file_id}`\n"
        f"Retrieve: `/get {file_id}`",
        parse_mode='Markdown'
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store videos"""
    global file_counter
    file_counter += 1
    
    file_id = str(file_counter)
    telegram_file_id = update.message.video.file_id
    file_name = update.message.video.file_name or f'video_{file_id}.mp4'
    
    file_storage[file_id] = {
        'telegram_id': telegram_file_id,
        'name': file_name,
        'type': 'video'
    }
    
    await update.message.reply_text(
        f"✅ Video saved!\n"
        f"📹 Name: `{file_name}`\n"
        f"🆔 ID: `{file_id}`\n"
        f"Retrieve: `/get {file_id}`",
        parse_mode='Markdown'
    )

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store audio files"""
    global file_counter
    file_counter += 1
    
    file_id = str(file_counter)
    telegram_file_id = update.message.audio.file_id
    file_name = update.message.audio.file_name or f'audio_{file_id}.mp3'
    
    file_storage[file_id] = {
        'telegram_id': telegram_file_id,
        'name': file_name,
        'type': 'audio'
    }
    
    await update.message.reply_text(
        f"✅ Audio saved!\n"
        f"🎵 Name: `{file_name}`\n"
        f"🆔 ID: `{file_id}`\n"
        f"Retrieve: `/get {file_id}`",
        parse_mode='Markdown'
    )

def main():
    """Start the bot"""
    # Application create karo
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_files))
    application.add_handler(CommandHandler("get", get_file))
    
    # File handlers
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    
    # Bot start karo
    print("Bot is running... 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()