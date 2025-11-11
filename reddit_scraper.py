import praw
import logging
import pandas as pd
import datetime
import re
import os
from typing import Optional

# prefer environment variables for secrets
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "jrzWLEkHCPHLEKetfDFldA")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "DfVM8NPG9sD-A8a_9s5LIUGJ9PgpYQ")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "BrandSentimentTracker by /u/aadiiii45")

DEFAULT_MAX_POSTS = 20

logger = logging.getLogger(__name__)

def _safe_filename(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]+', '_', name).strip('_')

def fetch_reddit_posts(
    brand: str,
    max_posts: int = DEFAULT_MAX_POSTS,
    output_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch Reddit submissions matching `brand` and return a DataFrame.
    Writes a CSV to output_dir (or current dir) and returns the DataFrame.
    """
    logger.info(f"Starting Reddit fetch for brand: {brand}")

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    except Exception as e:
        logger.error("Error creating Reddit client: %s", e)
        print(f"Error creating Reddit client: {e}")
        return pd.DataFrame([])

    posts = []
    subreddit = reddit.subreddit("all")
    try:
        for submission in subreddit.search(brand, limit=max_posts):
            created = datetime.datetime.utcfromtimestamp(submission.created_utc).isoformat() + "Z"
            posts.append({
                "title": submission.title,
                "selftext": submission.selftext,
                "url": submission.url,
                "created_utc": created,
                "score": getattr(submission, "score", None),
                "num_comments": getattr(submission, "num_comments", None),
                "subreddit": getattr(submission.subreddit, "display_name", None)
            })
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        print(f"Error fetching posts: {e}")

    df = pd.DataFrame(posts)

    safe_brand = _safe_filename(brand)
    filename = f"{safe_brand}_reddit_posts.csv"
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)

    df.to_csv(filename, index=False)
    logger.info(f"Saved {len(posts)} posts to {filename}")
    print(f"Saved {len(posts)} posts to {filename}")

    return df

# ---------------- Main Block ----------------
# if __name__ == "__main__":
#     logging.basicConfig(
#         filename="personal_reddit_scraper.log",
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s"
#     )

#     BRAND = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BRAND
#     MAX_POSTS = DEFAULT_MAX_POSTS

#     fetch_reddit_posts(BRAND, MAX_POSTS, output_dir=DEFAULT_OUTPUT_DIR)
