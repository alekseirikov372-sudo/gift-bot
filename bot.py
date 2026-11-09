import telebot
import random
import re
import sqlite3
import os

API_TOKEN = os.getenv("BOT_TOKEN", "8661420045:AAGT63LmpzBvysd5C-Ya3zs6GoSld2WGOFw")
bot = telebot.TeleBot(API_TOKEN)
DB_NAME = "offers.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            code TEXT PRIMARY KEY,
            gift_link TEXT,
            price TEXT,
            lang TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "<b>🤖 Бот офферов запущен в облаке!</b>\n\n"
        "Отправьте боту ссылку и цену в личку:\n"
        "<code>https://t.me/nft/CandyCane-112692 110 ru</code>",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: True)
def handle_private(message):
    raw_text = message.text or message.caption or ""
    if not raw_text or raw_text.startswith("/"):
        return

    parts = raw_text.replace("\n", " ").split()
    gift_link = ""
    price = "300"

    for part in parts:
        clean = part.strip("()[]{}<>.,!?;:")
        if "t.me/" in clean or "http" in clean:
            gift_link = clean
        elif clean.isdigit():
            price = clean

    if not gift_link and len(parts) > 0:
        for p in parts:
            if "t.me" in p:
                gift_link = p.strip("()[]{}<>.,!?;:")
                break

