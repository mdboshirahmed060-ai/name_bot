from flask import Flask
import threading
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

# --- Bot Code ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me your name, I will make it stylish 😎")

async def make_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    # stylish name banano
    stylish = f"★彡[{name}]彡★"
    await update.message.reply_text(f"Your stylish name: {stylish}")

if __name__ == '__main__':
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_name))
    print("Bot is running...")
    app_bot.run_polling()
