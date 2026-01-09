from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    
    if score > 0.05:
        label = 'Positive'
    elif score < -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
        
    return label, score
