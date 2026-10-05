from flask import Flask
import os, threading, random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"

NAMES = ["Aarav","Vihaan","Vivaan","Ananya","Diya","Sai","Arjun","Reyansh","Mohammed","Saanvi","Myra","Aadya","Ishaan","Kabir"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = random.sample(NAMES, 5)
    text = "✨ Tomar 5 ta sundor naam:\n\n" + "\n".join([f"{i+1}. {n}" for i,n in enumerate(names)])
    await update.message.reply_text(text)

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
