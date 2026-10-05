from flask import Flask
import threading, os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Alive!"
def run_flask(): app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_flask).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

COUNTRIES = [
"Afghanistan","Albania","Algeria","Andorra","Angola","Argentina","Armenia","Australia","Austria","Azerbaijan",
"Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia",
"Bosnia","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada",
"Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Croatia","Cuba","Cyprus","Czech Republic",
"Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia",
"Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guyana",
"Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan",
"Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg",
"Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar",
"Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Korea","North Macedonia","Norway",
"Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar",
"Romania","Russia","Rwanda","Saint Kitts","Saint Lucia","Samoa","San Marino","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syria",
"Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad","Tunisia","Turkey","Turkmenistan","Tuvalu",
"Uganda","Ukraine","UAE","UK","USA","Uruguay","Uzbekistan","Vanuatu","Vatican","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"
]

FIRST_BOY = ["Ahmed","Ali","Rahim","Karim","Arman","Aarav","Liam","Noah","James","John","David","Alex","Omar","Hassan","Mohammed"]
FIRST_GIRL = ["Fatima","Ayesha","Nusrat","Jannat","Olivia","Emma","Ava","Sophia","Mia","Zainab","Noor","Sara","Luna","Amelia"]
LAST_NAMES = ["Khan","Ahmed","Rahman","Smith","Johnson","Williams","Brown","Sharma","Patel","Kim","Lee","Garcia","Silva","Ali","Hossain"]

def gen_names(gender, count=30):
    pool = FIRST_BOY if gender=="boy" else FIRST_GIRL
    return [f"{random.choice(pool)} {random.choice(LAST_NAMES)}" for _ in range(count)]

def get_country_page(page=0, per_page=40):
    start = page*per_page
    end = start+per_page
    return COUNTRIES[start:end], page, len(COUNTRIES)//per_page

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    countries, page, total = get_country_page(0)
    btns = [[InlineKeyboardButton(c, callback_data=f"country_{c}")] for c in countries]
    btns.append([InlineKeyboardButton("➡️ Next 40 Country", callback_data=f"country_page_1")])
    await update.message.reply_text(f"🌍 195 ta desh (Page 1/{total+1}):\nDesh select koro:", reply_markup=InlineKeyboardMarkup(btns))

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data.startswith("country_page_"):
        page = int(data.split("_")[-1])
        countries, _, total = get_country_page(page)
        if not countries:
            await q.edit_message_text("✅ Sob desh sesh!")
            return
        btns = [[InlineKeyboardButton(c, callback_data=f"country_{c}")] for c in countries]
        nav = []
        if page>0: nav.append(InlineKeyboardButton("⬅️ Back", callback_data=f"country_page_{page-1}"))
        nav.append(InlineKeyboardButton("➡️ Next", callback_data=f"country_page_{page+1}"))
        btns.append(nav)
        await q.edit_message_text(f"🌍 195 ta desh (Page {page+1}):", reply_markup=InlineKeyboardMarkup(btns))

    elif data.startswith("country_") and not data.startswith("country_page"):
        country = data.split("_",1)[1]
        kb = [[InlineKeyboardButton("👦 Boy 400", callback_data=f"gender_boy_{country}_0"),
               InlineKeyboardButton("👧 Girl 400", callback_data=f"gender_girl_{country}_0")],
              [InlineKeyboardButton("🔙 All Country", callback_data="country_page_0")]]
        await q.edit_message_text(f"✅ {country}\nBoy naki Girl select koro:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("gender_"):
        _, gender, country, page = data.split("_")
        page=int(page)
        names = gen_names(gender, 30) # 30 kore, next chaple aro 30 = 400 porjonto jabe
        btns = [[InlineKeyboardButton(n, callback_data=f"copy_{n}")] for n in names]
        btns.append([InlineKeyboardButton("➡️ Next 400", callback_data=f"gender_{gender}_{country}_{page+1}")])
        btns.append([InlineKeyboardButton("🔙 Country List", callback_data="country_page_0")])
        await q.edit_message_text(f"🌍 {country} - {gender.title()} (Page {page+1})\nNam e click korle copy hobe:", reply_markup=InlineKeyboardMarkup(btns))

    elif data.startswith("copy_"):
        name = data.split("_",1)[1]
        await q.message.reply_text(f"📋 Copy:\n`{name}`", parse_mode="Markdown")

if __name__ == '__main__':
    b = ApplicationBuilder().token(BOT_TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CallbackQueryHandler(handler))
    b.run_polling()
