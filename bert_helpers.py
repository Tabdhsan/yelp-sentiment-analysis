from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

"""
AutoTokenizer converts a string into a sequence of numbers for the 
Natural Language Processing (NLP) model 
AutoModel provides architecture for loading NLP model
Torch extracts highest sequence results
"""

# Model Instantiation
tokenizer = AutoTokenizer.from_pretrained(
    "nlptown/bert-base-multilingual-uncased-sentiment"
)
model = AutoModelForSequenceClassification.from_pretrained(
    "nlptown/bert-base-multilingual-uncased-sentiment"
)


def get_sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors="pt")
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1
