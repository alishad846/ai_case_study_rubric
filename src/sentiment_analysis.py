from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def sentiment_score(text):
    blob = TextBlob(text)
    vader = analyzer.polarity_scores(text)
    # Combine polarity and vader positive
    score = (blob.sentiment.polarity + vader["pos"]) / 2
    return round(score, 2)
