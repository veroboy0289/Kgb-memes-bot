import os
import praw
import random
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="KGBMemeBot"
)

SUBREDDITS = ["CIA", "KGB", "funny", "memes", "ColdWar", "historymemes"]

def get_random_meme():
    subreddit = reddit.subreddit(random.choice(SUBREDDITS))
    posts = [post for post in subreddit.hot(limit=30) if not post.stickied and post.url.endswith(('.jpg', '.png', '.jpeg'))]
    if posts:
        return random.choice(posts).url
    return None