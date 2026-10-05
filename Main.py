from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()
