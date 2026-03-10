from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime, timezone, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_sentiment_data():
    newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    analyzer = SentimentIntensityAnalyzer()

    queries = [
        ("Bangalore real estate property", "bangalore"),
        ("Bangalore housing market rent", "bangalore"),
        ("Dubai real estate property", "dubai"),
        ("Dubai housing market rent", "dubai"),
    ]

    records = []
    from_date = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")

    for query, market in queries:
        try:
            response = newsapi.get_everything(
                q=query,
                from_param=from_date,
                language="en",
                sort_by="publishedAt",
                page_size=50
            )
            for article in response["articles"]:
                text = f"{article['title']} {article['description'] or ''}"
                scores = analyzer.polarity_scores(text)
                records.append({
                    "article_id": hash(article["url"]),
                    "market": market,
                    "title": article["title"][:200],
                    "source": article["source"]["name"],
                    "sentiment_compound": scores["compound"],
                    "sentiment_positive": scores["pos"],
                    "sentiment_negative": scores["neg"],
                    "sentiment_neutral": scores["neu"],
                    "published_at": article["publishedAt"],
                    "fetched_at": datetime.now(timezone.utc)
                })
        except Exception as e:
            print(f"Error fetching {query}: {e}")
            continue

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset=["article_id"])
    return df

if __name__ == "__main__":
    from db.loader import load_dataframe
    df = fetch_sentiment_data()
    print(df[["market", "title", "sentiment_compound"]].head(10))
    print(f"\nFetched {len(df)} articles")
    load_dataframe(df, "news_sentiment")