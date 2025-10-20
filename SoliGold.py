#!/usr/bin/env python3
import time
import requests
import telebot
from datetime import datetime
import logging

BOT_TOKEN = "xxxxxxxxxx:AAGIsNNwSm8Vxxxxx3C28uSqV8PQcVU"
CHANNEL_ID = -1003089928796
THREAD_ID = 87
INTERVAL = 600 
API_URL = "https://milli.gold/api/v1/public/milli-price/widget/external"

# ----- پیکربندی لاگ -----
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = telebot.TeleBot(BOT_TOKEN)

def get_daily_prices():
    """دریافت داده های DAILY از API"""
    try:
        resp = requests.get(API_URL, timeout=10).json()
        daily = resp["data"]["prices"]["DAILY"]
        if not daily:
            return None
        current = daily[-1]["value"]
        high = max(item["value"] for item in daily)
        low = min(item["value"] for item in daily)
        return current, high, low
    except Exception as e:
        logging.error(f"خطا در دریافت داده: {e}")
        return None

def main_loop():
    """ارسال قیمت ها به کانال هر ۱۰ دقیقه"""
    while True:
        prices = get_daily_prices()
        if prices:
            current, high, low = prices
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text = (
            f"ســلی‌گلــد ⚜️ SoliGold\n\n"
            f"[ ✨ ] نرخ فعلی هر گرم: {current:,} تومان\n\n"
            f"بالاترین: {high:,} تومان | پایین: {low:,} تومان"
            )

            try:
                bot.send_message(CHANNEL_ID, text, message_thread_id=THREAD_ID)
                logging.info(f"✅ پیام ارسال شد به {CHANNEL_ID}")
            except Exception as e:
                logging.error(f"❌ خطا در ارسال پیام: {e}")
        else:
            logging.warning("⚠️ داده های DAILY دریافت نشد.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    logging.info("ربات شروع به کار کرد ✅")
    main_loop()

