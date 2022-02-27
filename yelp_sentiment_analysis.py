#%%
import re
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import torch
from bs4 import BeautifulSoup
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Yelp Base Links
TOOLBOX_BASE_LINK = "https://www.yelp.com/biz/the-tool-box-new-york"
DTUT_BASE_LINK = "https://www.yelp.com/biz/dtut-new-york"

# Sentiment Analysis Prep
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

#%%
def create_dataframe_and_plot(base_link):
    # Creates a data frame with every review for a business
    all_reviews = get_all_reviews(base_link)
    df = pd.DataFrame(np.array(all_reviews), columns=["Date", "Review"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sentiment"] = df["Review"].apply(lambda x: get_sentiment_score(x[:512]))
    df = df.sort_values("Date")
    df["Year"] = pd.DatetimeIndex(df["Date"]).year
    year_sentiment = df[["Year", "Sentiment"]].copy()
    df2 = year_sentiment.groupby("Year").aggregate(["mean", "count"])
    year_mean_count_df = df2[df2.Sentiment["count"] > 5]
    year, mean = (
        year_mean_count_df["Sentiment"].index,
        year_mean_count_df["Sentiment"]["mean"],
    )
    plt.plot(year, mean)


def get_sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors="pt")
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def get_all_reviews(base_link):
    # Returns a list of reviews from every page
    all_reviews = []
    start = 0
    while True:
        single_page_reviews = get_single_page_reviews(base_link, start)
        if single_page_reviews:
            get_date_review_object(single_page_reviews, all_reviews)
            start += 10
            sleep(1.5)
        else:
            return all_reviews


def get_single_page_reviews(base_link, start):
    # Returns a list of reviews from a single page
    updated_link = base_link + "?start=" + str(start)
    r = requests.get(updated_link)
    soup = BeautifulSoup(r.text, "html.parser")
    single_page_reviews = soup.find_all("div", {"class": re.compile(".*review.*")})
    print(updated_link)
    return single_page_reviews if len(single_page_reviews) > 0 else False


def get_date_review_object(page_reviews_list, all_reviews):
    for review in page_reviews_list:
        date = review.find("span", {"class": "css-1e4fdj9"}).text
        comment = review.find("p", {"class": re.compile(".*comment.*")}).text.replace(
            "\xa0", ""
        )

        # NLP can only work with tokens upto 512 characters
        if len(comment) > 511:
            n = 511
            chunks = [[date, comment[i : i + n]] for i in range(0, len(comment), n)]
            all_reviews.extend(chunks)
        else:
            all_reviews.append([date, comment])


# %%

create_dataframe_and_plot(DTUT_BASE_LINK)
