import logging
import os
import random
import requests
import time
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUBREDDITS = ["funny", "memes", "dankmemes", "wholesomememes"]

bot = Bot(token=TELEGRAM_TOKEN)

def get_random_meme():
    headers = {"User-agent": "KGBMemeBot 1.0"}
    subreddit = random.choice(SUBREDDITS)
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return None
    posts = response.json()["data"]["children"]
    random.shuffle(posts)
    for post in posts:
        data = post["data"]
        image_url = data.get("url_overridden_by_dest")
        if image_url and image_url.lower().endswith((".jpg", ".jpeg", ".png")):
            return image_url
    return None

def generate_caption():
    prompt = "Придумай короткую и юмористическую подпись к мему в стиле токена KGB. Примеры: 'Купи KGB Token и стань майором', 'KGB следит за твоим кошельком'"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1.1,
        max_tokens=40,
    )
    return response["choices"][0]["message"]["content"].strip()

def post_meme():
    meme_url = get_random_meme()
    if meme_url:
        caption = generate_caption()
        try:
            bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption=caption)
            print(f"[{datetime.now()}] Posted meme: {meme_url}")
        except TelegramError as e:
            print(f"Failed to send meme: {e}")
    else:
        print("No suitable meme found.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    for hour in [8, 12, 16, 20]:
        scheduler.add_job(post_meme, "cron", hour=hour, minute=0)
    print("KGB Meme Bot started.")
    post_meme()  # Instant post on start
    scheduler.start()