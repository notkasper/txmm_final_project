import datetime as dt
from psaw import PushshiftAPI
import io
import json
import os


def getTickerPosts(ticker):
    api = PushshiftAPI()
    start_epoch = int(dt.datetime(2020, 1, 1).timestamp())
    end_epoch = int(dt.datetime(2021, 1, 1).timestamp())
    gen = api.search_submissions(
        q=ticker, subreddit='stocks', after=start_epoch, before=end_epoch)

    cache = []

    for c in gen:
        cache.append(c)
        print("collected: ", len(cache), " posts")

    with open("%s.json" % ticker, 'w') as outfile:
        json.dump(cache, outfile)


with open('tickers.json', 'r') as tickers_json_file:
    data = json.load(tickers_json_file)
    for ticker in data:
        getTickerPosts(ticker)
