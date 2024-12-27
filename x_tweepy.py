import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# APIキーとトークンを設定
API_KEY = os.getenv("X_API_KEY")
API_SECRET_KEY = os.getenv("X_SECRET_KEY")
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# クライアントを初期化
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# 災害関連のツイートを検索
def search_disaster_tweets_v2(keyword, count=10):
    try:
        # v2 APIで検索
        response = client.search_recent_tweets(query=keyword, max_results=count, tweet_fields=["created_at", "text"])
        tweets = response.data
        if tweets:
            for tweet in tweets:
                print(f"Tweet ID: {tweet.id}")
                print(f"Created at: {tweet.created_at}")
                print(f"Text: {tweet.text}")
                print("-" * 50)
        else:
            print("No tweets found.")
    except tweepy.TweepyException as e:
        print(f"Tweepy Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# 災害に関するキーワードで検索
search_disaster_tweets_v2("災害 OR 地震 OR 津波", count=10)