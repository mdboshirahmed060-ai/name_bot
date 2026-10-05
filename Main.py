import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

NAMES = ["Aarav", "Vihaan", "Rahim", "Karim", "Sakib", "Riya", "Mim", "Anika", "Boshir", "Tamim"]

@app.route('/')
def home():
    return "Bot is Alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamu Alaikum! 👋\nJekono okkhor likho, ami 5 ta sundor naam dibo!")

async def all_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = random.sample(NAMES, 5)
    text = "✨ Tomar 5 ta sundor naam:\n\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(names)])
    await update.message.reply_text(text)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, all_msg))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
