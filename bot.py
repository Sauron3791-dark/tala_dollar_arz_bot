import os
import requests
from telegram.ext import Updater, CommandHandler

# گرفتن توکن‌ها از متغیر محیطی
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("API_KEY")

# تابع گرفتن قیمت طلا و نقره
def get_prices():
    url = f"https://metals-api.com/api/latest?access_key={API_KEY}&base=USD&symbols=XAU,XAG"
    response = requests.get(url)
    data = response.json()
    if "success" in data and not data["success"]:
        return "❌ خطا: " + data["error"]["info"]
    else:
        rates = data["rates"]
        return f"🌟 قیمت طلا (XAU): {rates['XAU']} USD\n💎 قیمت نقره (XAG): {rates['XAG']} USD"

# دستور /start
def start(update, context):
    update.message.reply_text("سلام! 🤖 من ربات قیمت طلا و نقره هستم.\nبرای دیدن قیمت‌ها دستور /price رو بزن.")

# دستور /price
def price(update, context):
    prices = get_prices()
    update.message.reply_text(prices)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", price))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
