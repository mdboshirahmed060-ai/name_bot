from flask import Flask
import threading, os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Alive"
def run_flask(): app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_flask).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

COUNTRIES = ["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Croatia","Cuba","Cyprus","Czech","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Korea","North Macedonia","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts","Saint Lucia","Samoa","San Marino","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","UAE","UK","USA","Uruguay","Uzbekistan","Vanuatu","Vatican","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

BOY = ["Ahmed","Ali","Rahim","Arman","Sakib","Liam","Noah","James","David","Alex","Omar","Aarav","John"]
GIRL = ["Fatima","Ayesha","Nusrat","Jannat","Olivia","Emma","Ava","Sophia","Mia","Zainab","Sara","Noor","Anika"]
LAST = ["Khan","Ahmed","Rahman","Smith","Johnson","Brown","Sharma","Patel","Kim","Lee","Garcia","Ali","Hossain","Islam","Wilson"]

def make_400(page):
    random.seed(page*999)
    names=[]
    for i in range(400):
        first = random.choice(BOY) if i%2==0 else random.choice(GIRL)
        names.append(f"{first} {random.choice(LAST)}")
    random.seed()
    return names

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btns = [[InlineKeyboardButton(c, callback_data=f"C_{c}_0_0")] for c in COUNTRIES[:40]]
    btns.append([InlineKeyboardButton("➡️ Next 40 Country", callback_data="P_1")])
    await update.message.reply_text("🌍 195 Country - Desh select koro:", reply_markup=InlineKeyboardMarkup(btns))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d.startswith("P_"):
        p = int(d.split("_")[1])
        s = p*40
        e = s+40
        btns = [[InlineKeyboardButton(c, callback_data=f"C_{c}_0_0")] for c in COUNTRIES[s:e]]
        nav=[]
        if p>0: nav.append(InlineKeyboardButton("⬅️ Back", callback_data=f"P_{p-1}"))
        nav.append(InlineKeyboardButton("➡️ Next", callback_data=f"P_{p+1}"))
        btns.append(nav)
        await q.edit_message_text(f"🌍 Page {p+1}", reply_markup=InlineKeyboardMarkup(btns))

    elif d.startswith("C_"):
        _, country, main_p, sub_p = d.split("_")
        main_p=int(main_p); sub_p=int(sub_p)
        all_names = make_400(main_p)
        part = all_names[sub_p*50:(sub_p+1)*50]

        btns=[]
        for i in range(0, len(part), 2):
            row=[]
            for n in part[i:i+2]:
                # EI LINE TAI 1-CLICK COPY KORBE
                row.append(InlineKeyboardButton(n, copy_text=CopyTextButton(text=n)))
            btns.append(row)

        nav=[]
        if sub_p>0: nav.append(InlineKeyboardButton("⬅️ Back", callback_data=f"C_{country}_{main_p}_{sub_p-1}"))
        if sub_p<7: nav.append(InlineKeyboardButton("➡️ Next 50", callback_data=f"C_{country}_{main_p}_{sub_p+1}"))
        else: nav.append(InlineKeyboardButton("➡️ NEXT 400 🔥", callback_data=f"C_{country}_{main_p+1}_0"))
        btns.append(nav)
        btns.append([InlineKeyboardButton("🔙 Country", callback_data="P_0")])

        await q.edit_message_text(f"🌍 {country} - {main_p*400 + sub_p*50 + 1} to {main_p*400 + (sub_p+1)*50}\n👇 Nam e cap dile Copy hobe:", reply_markup=InlineKeyboardMarkup(btns))

if __name__ == '__main__':
    b = ApplicationBuilder().token(BOT_TOKEN).build()
    b.add_handler(CommandHandler("start", start))
    b.add_handler(CallbackQueryHandler(handle))
    b.run_polling()
