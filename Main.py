import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask for Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Name styles
def stylize_name(text):
    styles = {
        "1": f"★ {text} ★",
        "2": f"꧁ {text} ꧂",
        "3": f"【{text}】"
    }
    result = ""
    for k, v in styles.items():
        result += f"{k}. {v}\n"
    result += "\nTumar pochonder number likho!"
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nam pathao! Ami stylish baniye dibo!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if len(name) > 20:
        await update.message.reply_text("Nam ta choto dao vai!")
        return
    context.user_data['last_name'] = name
    await update.message.reply_text(stylize_name(name))

async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.strip()
    last_name = context.user_data.get('last_name')
    if not last_name:
        await update.message.reply_text("Age nam pathao!")
        return
    styles = {
        "1": f"★ {last_name} ★",
        "2": f"꧁ {last_name} ꧂",
        "3": f"【{last_name}】"
    }
    chosen = styles.get(num, "Number 1,2,3 er moddhe dao!")
    await update.message.reply_text(chosen)

def run_bot():
    if not BOT_TOKEN:
        print("BOT_TOKEN pai nai!")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex("^[1-3]$"), handle_number))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot Starting...")
    application.run_polling()

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
