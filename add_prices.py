# add prices to the preprocessed datagen
import requests
import json
from datetime import datetime
import time

# Base url for the requests
BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=__SYMBOL__&apikey=__KEY__"
# Top 10 tickers with most posts
TICKERS = ["AMD", "AMZN", "AAPL", "TEAM",
           "COST", "FAST", "FB", "GOOG", "GOOGL", "INTC"]
# API key
API_KEY = "PKWCK3S3NQZ0964G"
# API Rate limit
RATE_LIMIT = 5


# function to call the API and get the time series for a specific ticker
def getPrices(ticker):
    url = BASE_URL.replace("__SYMBOL__", ticker).replace("__KEY__", API_KEY)
    response = requests.get(url)
    if not response.status_code == 200:
        raise Exception("Failed API request")
    else:
        print("good response")
    response_json = response.json()
    key = "Weekly Time Series"
    if not key in response_json:
        print(response_json)
        raise Exception("Data missing from request")
    return response_json[key]


# make the format more compatible with how I saved the data in pre-processing
def reformatTickerTimeSeries(ticker_time_series):
    buffer = {}
    for key in ticker_time_series:
        if not "2020" in key:
            # we only want 2020 data anyway
            continue
        a_date = datetime.strptime(key, '%Y-%m-%d')
        week_number = str(a_date.isocalendar()[1])
        data = ticker_time_series[key]
        buffer[week_number] = data

    return buffer


# add prices to the pre-processed data, for each ticker, per week
def addPrices(weekly_ticker_sentiments, ticker, ticker_time_series):
    # The time series has keys in the form of '2021-01-14', so I change this to UTC, and then turn that into a week number using re-used code from a previous file
    # I then add the prices to each stock, for each week
    for week_nr in weekly_ticker_sentiments:
        # We dont have a value for each ticker for each week, but we still need the prices
        if not ticker in weekly_ticker_sentiments[week_nr]:
            weekly_ticker_sentiments[week_nr][ticker] = {}

        ticker_prices = ticker_time_series[week_nr]
        weekly_ticker_sentiments[week_nr][ticker]["prices"] = ticker_prices
    return weekly_ticker_sentiments


def main():
    with open("weekly_ticker_sentiments.json") as weekly_ticker_sentiments_json:
        weekly_ticker_sentiments = json.load(weekly_ticker_sentiments_json)
        counter = 0  # keep track of a counter to circumvent the 5 API calls per minute rate limit on the API
        for ticker in TICKERS:
            counter += 1
            ticker_time_series = reformatTickerTimeSeries(getPrices(ticker))
            weekly_ticker_sentiments = addPrices(
                weekly_ticker_sentiments, ticker, ticker_time_series)

            # circumvent rate limit
            if counter % RATE_LIMIT == 0 and not counter == len(TICKERS):
                print("Rate limit... waiting 60 seconds...")
                time.sleep(60)

        # save to a new file
        with open("final.json", 'w') as outfile:
            json.dump(weekly_ticker_sentiments, outfile)


if __name__ == "__main__":
    main()
