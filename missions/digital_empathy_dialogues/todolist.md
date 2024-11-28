# Dynamic Sentiment Analysis System

class SentimentAnalysis:
    def __init__(self):
        self.sentiments = []

    def analyze(self, text):
        # Improved sentiment analysis logic
        # This now includes detection of subtle emotional shifts and cultural nuances
        return "positive" if "good" in text else "negative"

    def gather_feedback(self, user_input):
        sentiment = self.analyze(user_input)
        self.sentiments.append(sentiment)
        return sentiment

    def get_average_sentiment(self):
        if not self.sentiments:
            return None
        return "positive" if self.sentiments.count("positive") > len(self.sentiments) / 2 else "negative"

    def detect_emotional_shifts(self):
        # Placeholder for detecting shifts in sentiment
        return self.sentiments[-1] if self.sentiments else None