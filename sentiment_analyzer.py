import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)

def get_sentiment(text: str) -> str:
    """
    Analyzes text and returns sentiment classification.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: 'Positive', 'Negative', or 'Neutral'
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def analyze_sentiment(input_file: str, output_dir: str) -> pd.DataFrame:
    """
    Analyze sentiment from an Excel/CSV file and generate visualizations.
    
    Args:
        input_file (str): Path to input Excel/CSV file
        output_dir (str): Directory to save output files
        
    Returns:
        pd.DataFrame: DataFrame with sentiment analysis results
    """
    logger.info(f"Starting sentiment analysis for {input_file}")
    
    try:
        if input_file.endswith('.xlsx'):
            df = pd.read_excel(input_file)
        else:
            df = pd.read_csv(input_file)
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {input_file}: {str(e)}")
        return None

    # Prepare text based on available columns
    df['title'] = df.get('title', '').fillna('')
    
    # Handle different column names for description/content
    if 'description' in df.columns:
        content_col = 'description'
    elif 'content' in df.columns:
        content_col = 'content'
    elif 'selftext' in df.columns:  # For Reddit posts
        content_col = 'selftext'
    else:
        content_col = None
        logger.warning("No content column found in the data")
    
    if content_col:
        df[content_col] = df[content_col].fillna('')
        df['full_text'] = df['title'] + ' ' + df[content_col]
    else:
        df['full_text'] = df['title']

    # Analyze sentiment
    df['sentiment'] = df['full_text'].apply(get_sentiment)

    # Generate visualization
    sentiment_counts = df['sentiment'].value_counts()
    
    plt.figure(figsize=(8, 8))
    sentiment_counts.plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=['green', 'red', 'lightgray']
    )
    plt.title('Brand Sentiment Analysis')
    plt.ylabel('')

    # Save results
    try:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        chart_path = os.path.join(output_dir, f'{base_name}_sentiment_chart.png')
        results_path = os.path.join(output_dir, f'{base_name}_with_sentiment.xlsx')
        
        plt.savefig(chart_path)
        plt.close()
        
        df.to_excel(results_path, index=False)
        
        logger.info(f"Sentiment analysis complete. Results saved to {output_dir}")
        print(f"\nSentiment Analysis Results for {base_name}:")
        print(sentiment_counts)
        print(f"Results saved to {output_dir}")
        
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        return None
    
    return df

if __name__ == "__main__":
    # Setup logging for standalone testing
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Test the function with sample data
    test_file = "sample_data.xlsx"
    test_output = "output"
    analyze_sentiment(test_file, test_output)