import twint
import pandas as pd
import os
import re
from typing import Optional
import nest_asyncio

# Needed to run Twint in scripts
nest_asyncio.apply()

# ---------------- Helper ----------------
def _safe_filename(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]+', '_', name).strip('_')

# ---------------- Main Function ----------------
def fetch_tweets_twint(
    brand: str,
    max_tweets: int = 50,
    output_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch tweets containing the given brand name using Twint.
    Returns a DataFrame and saves CSV if output_dir is provided.
    """
    c = twint.Config()
    c.Search = brand
    c.Limit = max_tweets
    c.Lang = "en"
    c.Hide_output = True
    c.Pandas = True  # Store results in Pandas DataFrame

    # Run Twint
    twint.run.Search(c)

    # Get tweets DataFrame
    df = twint.storage.panda.Tweets_df
    if df.empty:
        print(f"No tweets found for {brand}.")
        return df

    # Select useful columns
    df = df[["date", "username", "tweet", "link", "retweets_count", "likes_count"]]

    # Save CSV
    safe_brand = _safe_filename(brand)
    filename = f"{safe_brand}_tweets.csv"
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)

    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} tweets to {filename}")

    return df

# ---------------- Optional Direct Run ----------------
if __name__ == "__main__":
    import sys
    brand = sys.argv[1] if len(sys.argv) > 1 else "OpenAI"
    fetch_tweets_twint(brand, max_tweets=50)
