import os
import random
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
CHANNEL_ID = os.getenv("CHANNEL_ID")
BUY_URL = os.getenv("BOT_CONTRACT_URL")
SCHEDULE_HOUR = os.getenv("SCHEDULE_HOUR", "10:00")

memes = [
    "https://i.imgur.com/V0zPfRz.jpeg",
    "https://i.imgur.com/1TKKoZQ.jpeg",
    "https://i.imgur.com/BDGmLHg.jpeg"
]

captions = [
    "KGB is watching your wallet 👁️",
    "CIA didn't see this one coming...",
    "$KGB – the token they don't want you to know about.",
    "When you mix crypto with Cold War nostalgia 😎"
]

def post_meme():
    meme_url = random.choice(memes)
    caption = random.choice(captions)
    button = InlineKeyboardButton("Buy $KGB", url=BUY_URL)
    reply_markup = InlineKeyboardMarkup([[button]])
    bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption=caption, reply_markup=reply_markup)

if __name__ == "__main__":
    hour, minute = map(int, SCHEDULE_HOUR.split(":"))
    scheduler = BlockingScheduler()
    scheduler.add_job(post_meme, trigger="cron", hour=hour, minute=minute)
    post_meme()
    scheduler.start()