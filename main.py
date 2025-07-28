import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv
from reddit import get_random_meme
from captions import get_caption
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

async def post_meme():
    meme_url = get_random_meme()
    caption = get_caption()
    if meme_url:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=meme_url, caption=caption)

def main():
    scheduler.add_job(lambda: asyncio.create_task(post_meme()), 'interval', hours=6)
    scheduler.start()
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()