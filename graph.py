import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# loop over each week
# for each ticker
# get that tickers price from the next week
# check if the sentiment was correct/incorrect/neutral
# add that result to a buffer that contains correct/incorrect/neutral counters for each stock
# generate a bar chart, with 3 bars for each ticker.

TICKERS = ["AMD", "AMZN", "AAPL", "TEAM",
           "COST", "FAST", "FB", "GOOG", "GOOGL", "INTC"]

with open("final.json") as final_json:
    data = json.load(final_json)
    buffer = {}

    # overall stats
    correct = 0
    neutral = 0
    incorrect = 0

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for week_nr in range(1, len(data.keys())):
        current_week = str(week_nr)
        next_week = str(week_nr + 1)
        for ticker in TICKERS:
            if not ticker in buffer:
                buffer[ticker] = {
                    "correct": 0,
                    "neutral": 0,
                    "incorrect": 0
                }
            if not "compound" in data[current_week][ticker]:
                continue
            current_week_price = data[current_week][ticker]["prices"]["4. close"]
            next_week_price = data[next_week][ticker]["prices"]["4. close"]
            compound_sentiment = data[current_week][ticker]["compound"]
            if next_week_price > current_week_price and compound_sentiment >= 0.05:
                correct += 1
                tp += 1
                buffer[ticker]["correct"] += 1
            elif next_week_price < current_week_price and compound_sentiment >= 0.05:
                incorrect += 1
                fp += 1
                buffer[ticker]["incorrect"] += 1

            elif next_week_price < current_week_price and compound_sentiment <= -0.05:
                correct += 1
                tn += 1
                buffer[ticker]["correct"] += 1
            elif next_week_price > current_week_price and compound_sentiment <= -0.05:
                fn += 1
                buffer[ticker]["incorrect"] += 1
                incorrect += 1
            else:
                incorrect += 1
                neutral += 1
                buffer[ticker]["neutral"] += 1

    print("correct", correct /
          (correct + incorrect) * 100, "%")

    print("tp", tp)
    print("fp", fp)
    print("tn", tn)
    print("fn", fn)

    print("precision", tp / (tp + fp))
    print("recall", tp / (tp + fn))

    print("accuracy", (tp + tn) / (tp + tn + fp + fn), "%")

    def plot_individual():
        labels = TICKERS
        corrects = [buffer[ticker]["correct"] for ticker in labels]
        incorrects = [buffer[ticker]["incorrect"] for ticker in labels]
        neutrals = [buffer[ticker]["neutral"] for ticker in labels]

        x = np.arange(len(labels))  # the label locations
        width = 0.2  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width, corrects, width,
                        label='Correct', color="green")
        rects2 = ax.bar(x, incorrects, width,
                        label='Incorrect', color="orange")
        rects3 = ax.bar(x + width, neutrals, width,
                        label='Neutral', color="grey")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('# Prediction')
        ax.set_title('Trend prediction by sentiment analysis')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        fig.tight_layout()

        plt.show()

    def plot_combined():
        labels = ["Total predictions"]
        corrects = correct
        incorrects = incorrect
        neutrals = neutral

        x = np.arange(len(labels))  # the label locations
        width = 0.2  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width, corrects, width,
                        label='Correct', color="green")
        rects2 = ax.bar(x, incorrects, width,
                        label='Incorrect', color="orange")
        rects3 = ax.bar(x + width, neutrals, width,
                        label='Neutral', color="grey")

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('# Prediction')
        ax.set_title('Trend prediction by sentiment analysis')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)

        fig.tight_layout()

        plt.show()

    # plot_combined()
    plot_individual()
