import nltk
import pandas as pd
import numpy as np
import twitter_info
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer



print('Positive sentiment > 0.15')
print('negative sentiment < 0.4')
plt.show()
def retrieve_stock_news_headlines(stock_ticker):
    # Replace this with your own code for retrieving stock news headlines for the given stock ticker

    headlines = twitter_info.twitter_look(stock_ticker)
    return headlines


def analyze_sentiment(text):
    analyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment



def classify_sentiment(sentiment):
    if sentiment > 0.15:
        return 'Positive'
    elif sentiment < 0.04:
        return 'Negative'
    else:
        return 'Neutral'



def analyze_stock_sentiment(stock_ticker):
    # Retrieve stock news headlines for the given stock ticker
    headlines = retrieve_stock_news_headlines(stock_ticker)

    # Analyze the sentiment of each headline
    sentiments = []
    for headline in headlines:
        sentiment = analyze_sentiment(headline)
        # Extract the compound score from the sentiment dictionary
        compound_score = sentiment['compound']
        sentiments.append(compound_score)
        average_sentiments = np.mean(sentiments)

    # Check if the sentiments list is empty
    if not sentiments:
        raise ValueError('No sentiment scores were computed for the given headlines')

    # Classify the overall sentiment as bullish, bearish, or neutral
    overall_sentiment = classify_sentiment(average_sentiments)
    return overall_sentiment, sentiments, average_sentiments


try:
    overall_sentiment, sentiments, avg = analyze_stock_sentiment('christmas')
    print(f'Overall sentiment: {overall_sentiment}')
    print(str(round(avg,2)))
    plt.hist(sentiments)
    plt.show()
except ValueError as e:
    print(e)

