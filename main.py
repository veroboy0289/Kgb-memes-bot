
import os
import asyncio
import logging
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncpraw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = "kgb_meme_bot"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

SUBREDDITS = ["kgb", "CIA", "spyring", "coldwar", "memes"]
POST_LIMIT = 20

bot = Bot(token=TELEGRAM_TOKEN)

async def fetch_and_post():
    reddit = asyncpraw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=REDDIT_USER_AGENT
    )

    for subreddit_name in SUBREDDITS:
        subreddit = await reddit.subreddit(subreddit_name)
        async for post in subreddit.hot(limit=POST_LIMIT):
            if post.url.endswith((".jpg", ".png", ".jpeg")) and not post.stickied:
                try:
                    await bot.send_photo(
                        chat_id=TELEGRAM_CHANNEL_ID,
                        photo=post.url,
                        caption=post.title[:1024]
                    )
                    logger.info(f"Posted meme from r/{subreddit_name}: {post.title}")
                    break  # Публикуем только 1 мем за раз
                except Exception as e:
                    logger.error(f"Failed to send meme: {e}")
                break

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_post, "interval", hours=6)  # 4 раза в день
    scheduler.start()
    logger.info("Bot started and scheduler running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
