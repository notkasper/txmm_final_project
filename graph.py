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
    weekly_corrects = []
    weekly_incorrects = []

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
        weekly_correct = 0
        weekly_incorrect = 0
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
                weekly_correct += 1
            elif next_week_price < current_week_price and compound_sentiment >= 0.05:
                incorrect += 1
                fp += 1
                buffer[ticker]["incorrect"] += 1
                weekly_incorrect += 1
            elif next_week_price < current_week_price and compound_sentiment <= -0.05:
                correct += 1
                tn += 1
                buffer[ticker]["correct"] += 1
                weekly_correct += 1
            elif next_week_price > current_week_price and compound_sentiment <= -0.05:
                fn += 1
                buffer[ticker]["incorrect"] += 1
                incorrect += 1
                weekly_incorrect += 1
            else:
                incorrect += 1
                neutral += 1
                buffer[ticker]["neutral"] += 1
        weekly_corrects.append(weekly_correct)
        weekly_incorrects.append(weekly_incorrect)

    print("total predictions", correct + neutral + incorrect)
    print("correct", correct /
          (correct + incorrect) * 100, "%")

    print("tp", tp)
    print("fp", fp)
    print("tn", tn)
    print("fn", fn)

    print("precision", tp / (tp + fp))
    print("recall", tp / (tp + fn))

    print("accuracy", (tp + tn) / (tp + tn + fp + fn), "%")

    def plot_weekly_corrects():
        labels = range(len(weekly_corrects))

        x = np.arange(len(labels))  # the label locations

        fig, ax = plt.subplots()
        ax.plot(labels, weekly_corrects)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Correct predictions')
        ax.set_xlabel('Week number')
        ax.set_title('Correct predictions on a weekly basis')
        ax.set_xticks(x)

        fig.tight_layout()

        plt.show()

    def plot_monthly_predictions():
        labels = range(round(len(weekly_corrects) / 4))

        x = np.arange(len(labels))  # the label locations
        monthly = []

        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        totals = np.add(weekly_corrects, weekly_incorrects)
        monthly_chunks = list(chunks(totals, 4))
        ys = [sum(chunk) for chunk in monthly_chunks]

        fig, ax = plt.subplots()
        ax.plot(labels, ys, color="green",  linestyle='--',
                marker='o', label='Total number of predictions')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Total predictions')
        ax.set_xlabel('Chunk number')
        ax.set_title('Total number of predictions per chunk')
        ax.set_xticks(x)
        ax.set_ylim([0, 50])
        ax.legend()

        fig.tight_layout()

        plt.show()

    def plot_monthly_corrects():
        labels = range(round(len(weekly_corrects) / 4))

        x = np.arange(len(labels))  # the label locations
        monthly = []

        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        correct_factors = []
        i = 0
        for i in range(len(weekly_corrects)):
            total = weekly_corrects[i] + weekly_incorrects[i]
            factor = weekly_corrects[i] / total * 100
            correct_factors.append(factor)

        monthly_chunks = list(chunks(correct_factors, 4))
        ys = [round(sum(chunk) / 4) for chunk in monthly_chunks]

        fig, ax = plt.subplots()
        ax.plot(labels, ys, color="green",  linestyle='--',
                marker='o', label='Prediction')

        baseline = np.full(len(labels), 50,)

        ax.plot(labels, baseline, color="grey",
                linestyle='dashed', label='Chance')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Correct predictions in %')
        ax.set_xlabel('Chunk number')
        ax.set_title('Correct predictions per chunk (4 weeks)')
        ax.set_xticks(x)
        ax.set_ylim([0, 100])
        ax.legend()

        fig.tight_layout()

        plt.show()

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

    # plot_monthly_corrects()
    # plot_weekly_corrects()
    # plot_combined()
    # plot_individual()
    plot_monthly_predictions()
