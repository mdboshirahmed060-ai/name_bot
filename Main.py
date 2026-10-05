from flask import Flask
import threading
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Alive!"
def run_flask(): app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_flask).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Country list
COUNTRIES = ["Bangladesh", "India", "Pakistan", "USA", "UK", "Canada", "Japan", "Korea", "Turkey", "Saudi Arabia", "Germany", "France", "Brazil", "Australia", "Italy"]

# Fake first/last names for demo - you can add more
FIRST_BOY = ["Arman", "Rahim", "Karim", "Fahim", "Sakib", "Aarav", "Liam", "Noah", "Ahmed", "Ali", "John", "David", "Alex", "Chris", "James"]
FIRST_GIRL = ["Fatima", "Ayesha", "Nusrat", "Jannat", "Mim", "Saanvi", "Olivia", "Emma", "Ava", "Zainab", "Sophia", "Isabella", "Mia", "Luna"]
LAST_NAMES = ["Khan", "Ahmed", "Rahman", "Islam", "Hossain", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Sharma", "Patel", "Kim", "Lee", "Silva"]

def generate_names(gender, page, count=50): # 50 kore dekhabe, 8 page = 400
    first_pool = FIRST_BOY if gender == "boy" else FIRST_GIRL
    names = []
    start = page * count
    for i in range(count):
        f = random.choice(first_pool)
        l = random.choice(LAST_NAMES)
        names.append(f"{f} {l}")
    return names

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = []
    row = []
    for c in COUNTRIES:
        row.append(InlineKeyboardButton(c, callback_data=f"country_{c}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)
    await update.message.reply_text("🌍 Country select koro:", reply_markup=InlineKeyboardMarkup(buttons))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("country_"):
        country = data.split("_", 1)[1]
        kb = [
            [InlineKeyboardButton("👦 Boy", callback_data=f"gender_boy_{country}_0"),
             InlineKeyboardButton("👧 Girl", callback_data=f"gender_girl_{country}_0")]
        ]
        await query.edit_message_text(f"✅ {country} select korcho!\nBoy naki Girl?", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("gender_"):
        _, gender, country, page = data.split("_")
        page = int(page)
        names = generate_names(gender, page)

        buttons = []
        row = []
        for n in names:
            # name e click korle copy hobe
            row.append(InlineKeyboardButton(n, callback_data=f"copy_{n}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)

        # Next button - 400 por por next
        buttons.append([InlineKeyboardButton("➡️ Next 400", callback_data=f"gender_{gender}_{country}_{page+1}")])
        buttons.append([InlineKeyboardButton("🔙 Back to Country", callback_data="back")])

        await query.edit_message_text(f"🌍 {country} - {gender.title()} Names (Page {page+1}):\n\nNam e click korle copy er jonno alada pathabo 👇", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("copy_"):
        name = data.split("_", 1)[1]
        await query.message.reply_text(f"📋 Copy koro:\n`{name}`\n\nTap kore dhore rakho copy hobe!", parse_mode="Markdown")

    elif data == "back":
        buttons = []
        row = []
        for c in COUNTRIES:
            row.append(InlineKeyboardButton(c, callback_data=f"country_{c}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row: buttons.append(row)
        await query.edit_message_text("🌍 Country select koro:", reply_markup=InlineKeyboardMarkup(buttons))

if __name__ == '__main__':
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(button_handler))
    print("Pro Bot Running...")
    bot.run_polling()
