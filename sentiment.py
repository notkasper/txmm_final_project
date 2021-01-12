from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import date, timedelta, datetime, timezone
import datetime as dt
import time
import json
import numpy as np
import string
import math
import spacy
import nltk
import re

nltk.download('vader_lexicon')
nltk.download('stopwords')

# Top 10 tickers with most posts
TICKERS = ["AMD", "AMZN", "AAPL", "TEAM",
           "COST", "FAST", "FB", "GOOG", "GOOGL", "INTC"]


def main():
    # setup sentiment analysis tools
    sid = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words("english"))
    buffer = {}

    # for each day, calculate the sentiment for each ticker
    with open("sorted_posts.json") as posts_json:
        sorted_posts = json.load(posts_json)
        for date_utc in sorted_posts:
            buffer[date_utc] = {}
            for ticker in TICKERS:
                buffer[date_utc][ticker] = {}
                if ticker in sorted_posts[date_utc]:
                    posts = sorted_posts[date_utc][ticker]
                    buffer[date_utc][ticker]["post_texts"] = []
                    sentiments = []

                    # for each post of a specific ticker on a specific day
                    scores = []
                    for post in posts:
                        if not "selftext" in post:
                            continue
                        text = post["selftext"]
                        buffer[date_utc][ticker]["post_texts"].append(text)
                        score = sid.polarity_scores(text)
                        scores.append(score)

                    # save scores + averages
                    buffer[date_utc][ticker]["data"] = {}
                    buffer[date_utc][ticker]["data"]["scores"] = scores
                    buffer[date_utc][ticker]["data"]["pos_average"] = np.mean(
                        [score["pos"] for score in scores])
                    buffer[date_utc][ticker]["data"]["neg_average"] = np.mean(
                        [score["neg"] for score in scores])
                    buffer[date_utc][ticker]["data"]["compound_average"] = np.mean(
                        [score["compound"] for score in scores])
                    buffer[date_utc][ticker]["data"]["neu_average"] = np.mean(
                        [score["neu"] for score in scores])
        # save to a new file
        with open("posts_with_scores.json", 'w') as outfile:
            json.dump(buffer, outfile)


if __name__ == "__main__":
    main()
