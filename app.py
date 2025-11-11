import os
import sys
import argparse
import logging
from pathlib import Path


# ensure project root is importable
ROOT = Path(__file__).parent.parent.absolute()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scraper.news_scraper import fetch_news
from scraper.reddit_scraper import fetch_reddit_posts
from scraper.data_handler import clean_Data_saveto_exel
from nlp.sentiment_analyzer import analyze_sentiment

# Set up logging
log_file = ROOT / "scraper_run.log"
logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def process_brand_data(brand: str, max_posts: int, max_articles: int, output_dir: Path) -> tuple:
    """Process both news and reddit data for a given brand"""
    news_df = fetch_news(brand, language="en", max_articles=max_articles, output_dir=str(output_dir))
    reddit_df = fetch_reddit_posts(brand, max_posts=max_posts, output_dir=str(output_dir))
    
    # Process each CSV file for sentiment
    for file_path in output_dir.glob(f"{brand}*.csv"):
        if file_path.exists():
            try:
                # First clean the data
                cleaned_df = clean_Data_saveto_exel(str(file_path))
                if cleaned_df is not None:
                    # Then analyze sentiment for the cleaned Excel file
                    excel_path = str(file_path).replace('.csv', '_cleaned.xlsx')
                    if os.path.exists(excel_path):
                        sentiment_df = analyze_sentiment(excel_path, str(output_dir))
                        if sentiment_df is None:
                            logger.warning(f"Sentiment analysis failed for {excel_path}")
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                continue

    return news_df, reddit_df

def main():
    parser = argparse.ArgumentParser(description="Fetch news and reddit posts for a brand")
    brand = input("Enter the brand to search for (default: OpenAI): ") or "OpenAI"
    parser.add_argument("--brand", "-b", 
                       default=brand,  # Add default value
                       help="Brand to search for (default: OpenAI)")
    parser.add_argument("--max-posts", type=int, default=20, help="Max reddit posts to fetch")
    parser.add_argument("--max-articles", type=int, default=10, help="Max news articles to fetch")
    parser.add_argument("--output-dir", "-o", default="data", help="Directory to save outputs")
    args = parser.parse_args()

    # Setup output directory
    output_dir = Path(args.output_dir).absolute()
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting full scrape for brand={args.brand}")
    
    try:
        # Fetch and process data
        news_df, reddit_df = process_brand_data(
            args.brand, 
            args.max_posts, 
            args.max_articles, 
            output_dir
        )

        # Print results
        print(f"\nResults for brand '{args.brand}':")
        print(f"News articles fetched: {len(news_df)}")
        print(f"Reddit posts fetched: {len(reddit_df)}")
        print(f"Data and sentiment analysis saved to: {output_dir}")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

    logger.info(f"Finished full scrape for brand={args.brand}")

if __name__ == "__main__":
    main()