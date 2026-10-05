from flask import Flask
import threading, os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running 24h"
def run_flask(): app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_flask).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

COUNTRIES = ["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Croatia","Cuba","Cyprus","Czech","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Korea","North Macedonia","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts","Saint Lucia","Samoa","San Marino","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","UAE","UK","USA","Uruguay","Uzbekistan","Vanuatu","Vatican","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

BOY_FIRST = ["Ahmed","Ali","Rahim","Arman","Sakib","Liam","Noah","James","David","Alex","Omar","Hassan","Aarav","John","Chris"]
GIRL_FIRST = ["Fatima","Ayesha","Nusrat","Jannat","Olivia","Emma","Ava","Sophia","Mia","Zainab","Sara","Noor","Amelia","Luna","Saanvi"]
LAST = ["Khan","Ahmed","Rahman","Smith","Johnson","Williams","Brown","Sharma","Patel","Kim","Lee","Garcia","Ali","Hossain","Wilson","Islam"]

def make_400_names(page):
    random.seed(page + 12345) # proti page e notun 400
    names = []
    for i in range(400):
        if i % 2 == 0:
            f = random.choice(BOY_FIRST)
        else:
            f = random.choice(GIRL_FIRST)
        l = random.choice(LAST)
        names.append(f"{f} {l}")
    random.seed()
    return names

def get_names_slice(full_list, sub_page, per=50):
    s = sub_page * per
    return full_list[s:s+per]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btns = []
    for c in COUNTRIES[:40]:
        btns.append([InlineKeyboardButton(c, callback_data=f"COUNTRY_{c}_0_0")])
    btns.append([InlineKeyboardButton("➡️ Next 40 Country", callback_data="CPAGE_1")])
    await update.message.reply_text("🌍 195 Country - Select koro:", reply_markup=InlineKeyboardMarkup(btns))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data.startswith("CPAGE_"):
        p = int(data.split("_")[1])
        start_idx = p*40
        end_idx = start_idx+40
        slice_c = COUNTRIES[start_idx:end_idx]
        btns = [[InlineKeyboardButton(c, callback_data=f"COUNTRY_{c}_0_0")] for c in slice_c]
        nav = []
        if p>0: nav.append(InlineKeyboardButton("⬅️ Back", callback_data=f"CPAGE_{p-1}"))
        nav.append(InlineKeyboardButton("➡️ Next", callback_data=f"CPAGE_{p+1}"))
        btns.append(nav)
        await q.edit_message_text(f"🌍 Country Page {p+1}", reply_markup=InlineKeyboardMarkup(btns))

    elif data.startswith("COUNTRY_"):
        _, country, main_page, sub_page = data.split("_")
        main_page = int(main_page)
        sub_page = int(sub_page)

        full_400 = make_400_names(main_page)
        names_50 = get_names_slice(full_400, sub_page, 50)

        btns = []
        row=[]
        for n in names_50:
            row.append(InlineKeyboardButton(n, callback_data=f"COPY_{n}"))
            if len(row)==2:
                btns.append(row)
                row=[]
        if row: btns.append(row)

        # Navigation
        nav=[]
        if sub_page > 0:
            nav.append(InlineKeyboardButton("⬅️ Back", callback_data=f"COUNTRY_{country}_{main_page}_{sub_page-1}"))

        if sub_page < 7: # 0-7 = 8 page = 400 nam
            nav.append(InlineKeyboardButton("➡️ Next 50", callback_data=f"COUNTRY_{country}_{main_page}_{sub_page+1}"))
        else:
            nav.append(InlineKeyboardButton("➡️ NEXT 400 🔥", callback_data=f"COUNTRY_{country}_{main_page+1}_0"))

        btns.append(nav)
        btns.append([InlineKeyboardButton("🔙 Country List", callback_data="CPAGE_0")])

        await q.edit_message_text(f"🌍 {country} - {main_page*400 + sub_page*50 + 1} to {main_page*400 + (sub_page+1)*50} Names\nNam e cap dile Copy hobe:", reply_markup=InlineKeyboardMarkup(btns))

    elif data.startswith("COPY_"):
        name = data.split("_", 1)[1]
        # Eita te upore Copy icon asbe
        await q.message.reply_text(f"📋 Copy koro:\n```\n{name}\n```", parse_mode="Markdown")

if __name__ == '__main__':
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(handle))
    print("195 Country Bot Ready")
    app_bot.run_polling()
