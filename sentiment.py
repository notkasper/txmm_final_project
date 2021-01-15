from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import date, timedelta, datetime, timezone
from datetime import datetime
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

    # for each week, calculate the sentiment for each ticker
    with open("sorted_posts.json") as posts_json:
        sorted_posts = json.load(posts_json)
        for date_utc in sorted_posts:
            a_date = datetime.fromtimestamp(int(date_utc))
            week_number = a_date.isocalendar()[1]
            buffer[week_number] = {}
            print("week nr", week_number)
            for ticker in TICKERS:
                buffer[week_number][ticker] = {}
                if ticker in sorted_posts[date_utc]:
                    posts = sorted_posts[date_utc][ticker]
                    buffer[week_number][ticker]["post_texts"] = []
                    sentiments = []

                    # for each post of a specific ticker on a specific day
                    scores = []
                    for post in posts:
                        if not "selftext" in post:
                            continue
                        text = post["selftext"]
                        buffer[week_number][ticker]["post_texts"].append(text)
                        score = sid.polarity_scores(text)
                        scores.append(score)
                    if not "scores" in buffer[week_number][ticker]:
                        buffer[week_number][ticker]["scores"] = []
                    buffer[week_number][ticker]["scores"] = buffer[week_number][ticker]["scores"] + scores

        weekly_averages = {}
        for week_number in buffer:
            weekly_averages[week_number] = {}
            for ticker in buffer[week_number]:
                if not "scores" in buffer[week_number][ticker]:
                    continue
                scores = buffer[week_number][ticker]["scores"]
                ticker_weekly_averages = {
                    "pos": round(np.mean([score["pos"] for score in scores]), 2),
                    "neg": round(np.mean([score["neg"] for score in scores]), 2),
                    "compound": round(np.mean([score["compound"] for score in scores]), 2)
                }
                weekly_averages[week_number][ticker] = ticker_weekly_averages

        # save to a new file
        with open("weekly_ticker_sentiments.json", 'w') as outfile:
            json.dump(weekly_averages, outfile)


if __name__ == "__main__":
    main()
