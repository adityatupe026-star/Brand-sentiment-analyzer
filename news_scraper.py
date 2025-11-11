import logging
import pandas as pd
import requests
import os
import re
from typing import Optional

# read API key from environment if available
API_KEY = os.getenv("NEWSAPI_KEY", "4e5f03adb32f4d65ad6b4c1b637c86ed")

logger = logging.getLogger(__name__)

def _safe_filename(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]+', '_', name).strip('_')

def fetch_news(
    brand: str,
    language: str = "en",
    max_articles: int = 10,
    output_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch news articles for a brand using NewsAPI and return a DataFrame.
    Writes a CSV to output_dir (or current dir) and returns the DataFrame.
    """
    logger.info("Starting news fetch process")
    url = f"https://newsapi.org/v2/everything?q={brand}&language={language}&pageSize={max_articles}&apiKey={API_KEY}"
    logger.info(f"Fetching news articles for brand: {brand}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error("Error fetching news: %s", e)
        print(f"Error fetching news: {e}")
        return pd.DataFrame([])

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "content": article.get("content"),
            "url": article.get("url"),
            "published_at": article.get("publishedAt"),
            "source": article.get("source", {}).get("name")
        })

    df = pd.DataFrame(articles)

    safe_brand = _safe_filename(brand)
    filename = f"{safe_brand}_news.csv"
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)

    df.to_csv(filename, index=False)
    logger.info(f"Saved {len(articles)} articles to {filename}")
    print(f"Saved {len(articles)} articles to {filename}")

    return df

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     fetch_news("Open", language, max_articles)