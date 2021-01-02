import json
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")

FILENAME = "stock_posts.json"

analyzer = SentimentIntensityAnalyzer()
with open(FILENAME, encoding="utf8") as json_file:
    data = json.load(json_file)

    for key in data.keys():
        for post in data[key]:
            text = post["selftext"]
            doc = nlp(text)
            token_list = [token for token in doc]
            lemmas = [token.lemma_ for token in doc if not token.is_stop]
            vs = analyzer.polarity_scores(text)
            print(text)
            print(vs)
            print("=============================================")
            break
