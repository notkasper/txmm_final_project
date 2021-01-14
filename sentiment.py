import datetime as dt
from datetime import date, timedelta, datetime, timezone
import time
import json
import math
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Top 10 tickers with most posts
TICKERS = ["AMD", "AMZN", "AAPL", "TEAM",
           "COST", "FAST", "FB", "GOOG", "GOOGL", "INTC"]
# Earliest bin date
START_DATE = dt.datetime(2020, 1, 1)
# Latest bin date
END_DATE = dt.datetime(2020, 11, 30)
# Seconds in a day which translated to bin size
BIN_SIZE_UTC = 86400

# We only need some of the data in the raw post, specifically the only dictionary in ther


def getPostData(post_raw):
    post_dict = None
    for element in post_raw:
        if type(element) is dict:
            post_dict = element
    return post_dict


# For each day between a start and end date, for each day between those dates, get posts from that day and sort them by ticker
def main():
    nlp = spacy.load("en_core_web_sm")
    analyzer = SentimentIntensityAnalyzer()
    delta = timedelta(days=1)
    start_date = int(START_DATE.replace(
        tzinfo=timezone.utc).timestamp())
    end_date = int(END_DATE.replace(
        tzinfo=timezone.utc).timestamp())

    days = int((end_date-start_date) / BIN_SIZE_UTC)
    buffer = {}
    for ticker in TICKERS:
        with open("./data/" + ticker + ".json") as posts_json:
            posts = json.load(posts_json)
            for post in posts:
                post_data = getPostData(post)
                utc = post_data["created_utc"]
                day = math.floor((utc - start_date) /
                                 BIN_SIZE_UTC) * BIN_SIZE_UTC + start_date
                if not day in buffer:
                    buffer[day] = {}
                if not ticker in buffer[day]:
                    buffer[day][ticker] = []
                buffer[day][ticker].append(post_data)
    with open("sorted_posts.json", 'w') as outfile:
        json.dump(buffer, outfile)


def displayTickerCount(ticker):
    with open("sorted_posts.json", 'r') as stonks_json:
        stonks = json.load(stonks_json)
        counter = 0
        for key in stonks.keys():
            tickers_and_posts = stonks[key]
            if ticker in tickers_and_posts:
                posts = tickers_and_posts[ticker]
                counter += len(posts)
        print("total ", ticker, " posts: ", counter)


if __name__ == "__main__":
    main()
    for ticker in TICKERS:
        displayTickerCount(ticker)
