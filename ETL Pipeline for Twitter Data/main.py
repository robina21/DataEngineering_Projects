import tweepy
from datetime import datetime
import re
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret, db_user, db_password, db_host, db_name

# Twitter API credentials
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# PostgreSQL database connection
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Tweet object for SQLAlchemy
class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_handle = Column(String)
    timestamp = Column(DateTime)
    likes = Column(Integer)
    retweets = Column(Integer)

    def __repr__(self):
        return f'<Tweet(id={self.id}, text={self.text}, user_handle={self.user_handle}, timestamp={self.timestamp}, likes={self.likes}, retweets={self.retweets})>'

# Clean tweet text
def clean_tweet(tweet_text):
    clean_text = re.sub(r'http\S+', '', tweet_text) # remove URLs
    clean_text = re.sub(r'[^\w\s]','', clean_text) # remove special characters
    clean_text = clean_text.lower() # lowercase text
    return clean_text

# Extract, transform, and load pipeline
def etl_pipeline():
    # Extract
    search_keywords = ['#COVID19'] # search keywords for tweets
    tweets = api.search(q=search_keywords, lang='en', tweet_mode='extended', count=100) # retrieve latest 100 tweets

    # Transform
    transformed_tweets = []
    for tweet in tweets:
        cleaned_text = clean_tweet(tweet.full_text)
        transformed_tweet = {
            'text': cleaned_text,
            'user_handle': tweet.user.screen_name,
            'timestamp': datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S'),
            'likes': tweet.favorite_count,
            'retweets': tweet.retweet_count
        }
        transformed_tweets.append(transformed_tweet)

    # Load
    for tweet in transformed_tweets:
        new_tweet = Tweet(text=tweet['text'], user_handle=tweet['user_handle'], timestamp=tweet['timestamp'], likes=tweet['likes'], retweets=tweet['retweets'])
        session.add(new_tweet)
    session.commit()

if __name__ == '__main__':
    etl_pipeline()
