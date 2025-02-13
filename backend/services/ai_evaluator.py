from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import textstat

def evaluate_text(text: str):
    """
    Evaluate the given text using sentiment analysis and readability scoring.
    
    Returns:
        dict: A dictionary containing sentiment scores and readability score.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    readability = textstat.flesch_reading_ease(text)
    
    return {
        "sentiment": sentiment,
        "readability": readability
    }
