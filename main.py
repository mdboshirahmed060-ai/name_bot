
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token Render theke asbe
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN nai!")
    
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamu Alaikum! Nam likho, ami desh bole dibo!\nExample: Rahim")

async def check_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name:
        return
    # Simple logic
    if "rahim" in name.lower() or "karim" in name.lower():
        desh = "Bangladesh"
    else:
        desh = "All Country"
    await update.message.reply_text(f"{name} -> {desh} er nam hote pare!")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_name))
    print("Bot Starting...")
    application.run_polling()

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
