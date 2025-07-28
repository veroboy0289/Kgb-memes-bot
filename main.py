import logging
import os
import random
import requests
import schedule
import time
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = "kgb-meme-bot/0.1"

bot = Bot(token=BOT_TOKEN)

HEADERS = {"User-Agent": REDDIT_USER_AGENT}
AUTH = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)
DATA = {"grant_type": "client_credentials"}

auth_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=AUTH, data=DATA, headers=HEADERS)
TOKEN = auth_response.json()["access_token"]
HEADERS["Authorization"] = f"bearer {TOKEN}"

def get_meme_image():
    subreddits = ["PoliticalHumor", "MemesAgainstFascism", "shitposting", "MemeEconomy"]
    subreddit = random.choice(subreddits)
    url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit=25"
    res = requests.get(url, headers=HEADERS)
    posts = res.json()["data"]["children"]
    random.shuffle(posts)

    for post in posts:
        if post["data"]["post_hint"] == "image":
            return post["data"]["url"]
    return None

def get_caption():
    captions = [
        "Купи KGB Token и стань майором 🕵️‍♂️",
        "KGB следит за твоим кошельком 👀",
        "У тебя нет в кошельке KGB, зато ты есть в кармане у KGB 💼",
        "Один KGB Token — один шаг к мировой слежке 🌍",
    ]
    return random.choice(captions)

def post_meme():
    try:
        image_url = get_meme_image()
        caption = get_caption()
        if image_url:
            bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=caption)
            print("Meme posted successfully")
        else:
            print("No image meme found.")
    except TelegramError as e:
        logging.error(f"Telegram error: {e}")

# План: 4 раза в день
schedule.every().day.at("09:00").do(post_meme)
schedule.every().day.at("13:00").do(post_meme)
schedule.every().day.at("17:00").do(post_meme)
schedule.every().day.at("21:00").do(post_meme)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)