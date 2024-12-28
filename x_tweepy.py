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
        response = client.search_recent_tweets(
            query=keyword,
            max_results=count,
            tweet_fields=["created_at", "text"],
            expansions=["author_id"],
            user_fields=["username"]
        )
        
        tweets = response.data
        users = {user["id"]: user["username"] for user in response.includes["users"]}
        
        if tweets:
            result = []
            for tweet in tweets:
                username = users.get(tweet.author_id, "unknown_user")
                tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
                result.append({
                    "tweet_id": tweet.id,
                    "created_at": tweet.created_at,
                    "text": tweet.text,
                    "url": tweet_url
                })
            return result
        else:
            print("No tweets found.")
    except tweepy.TweepyException as e:
        print(f"Tweepy Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return []

# 災害に関するキーワードで検索
# print(search_disaster_tweets_v2("災害 OR 地震 OR 津波", count=10))
