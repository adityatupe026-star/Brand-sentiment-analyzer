# Brand Sentiment Analyzer 📊

A Python-based tool that analyzes text data (tweets, reviews, comments) to determine the **sentiment** toward a brand as **positive, negative, or neutral**.

---

## Features ✨
- Supports multiple text sources: CSV, Excel, or live input.
- Classifies sentiment using **NLP techniques**.
- Generates visualizations: pie charts, bar graphs of sentiment distribution.
- Easy to extend for multiple brands or custom datasets.
- Provides summary statistics: % positive, negative, and neutral sentiments.

---

## Tech Stack 🛠
- Python 3.x  
- Pandas, Numpy  
- NLTK / SpaCy / TextBlob / Transformers (depending on approach)  
- Matplotlib / Seaborn (for visualizations)  

---

## Installation ⚡

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-folder>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure your dataset is in a CSV or Excel format with a column containing text.

---

## Usage 🚀

1. Run the analyzer:
```bash
python sentiment_analyzer.py
```

2. Provide the path to your dataset or input text manually:
```
Enter CSV path: data/brand_tweets.csv
```

3. Get sentiment results and visualizations:
```
Positive: 45%
Neutral: 30%
Negative: 25%
```

4. Output can also be saved to CSV for further analysis.

---

## Example
```python
from sentiment_analyzer import analyze_sentiment

data = ["I love this brand!", "Their service is terrible.", "Average experience."]
results = analyze_sentiment(data)
print(results)
```

---

## Notes 📝
- Preprocessing steps include removing stopwords, punctuation, and lowercasing text.
- Model choice (TextBlob, VADER, or Transformers) can be swapped based on accuracy requirements.
- Can be extended for **real-time sentiment monitoring** on social media.

---

## Author ✍️
- Name: Your Name  
- GitHub: [yourusername](https://github.com/yourusername)  
- Email: your.email@example.com  

---

## License
Open-source project. Free to use and modify for learning or personal projects.