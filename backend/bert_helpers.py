"""
This script demonstrates sentiment analysis using a pre-trained BERT-based model.
"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Model and tokenizer instantiation
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)


def get_sentiment_score(review):
    """
    Analyzes the sentiment of a given review text.

    Args:
        review (str): The review text to be analyzed.

    Returns:
        int: Sentiment score in the range 1 to 5.
    """
    tokens = tokenizer.encode(review, return_tensors="pt")
    result = model(tokens)
    sentiment_score = torch.argmax(result.logits).item() + 1
    return sentiment_score


if __name__ == "__main__":
    review_text = "I really enjoyed this product. It exceeded my expectations!"
    sentiment_score = get_sentiment_score(review_text)
    print(f"Sentiment Score: {sentiment_score}")
