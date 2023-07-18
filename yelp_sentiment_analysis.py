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
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import io
import base64

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

global establishment_name

def create_dataframe_and_plot(base_link):
    # Creates a data frame with every review for a business
    all_reviews = get_all_reviews(base_link)
    print('allReciewcount',len(all_reviews))

    df = pd.DataFrame(np.array(all_reviews), columns=["Date", "Review"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sentiment"] = df["Review"].apply(lambda x: get_sentiment_score(x[:512]))
    df = df.sort_values("Date")
    df["Year"] = pd.DatetimeIndex(df["Date"]).year.astype(int)
    year_sentiment = df[["Year", "Sentiment"]].copy()
    df2 = year_sentiment.groupby("Year").aggregate(["mean", "count"])
    year_mean_count_df = df2[df2.Sentiment["count"] > 5]
    year, mean = (
        year_mean_count_df["Sentiment"].index.astype(int),
        year_mean_count_df["Sentiment"]["mean"],
    )
            
    # Set plot style 
    plt.style.use('seaborn')

    fig, ax = plt.subplots()

    # Plot line
    ax.plot(year, mean)

    # Axis aesthetics
    ax.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Label aesthetics
    ax.set_xlabel('Years', fontsize=14, x=-0.05) 
    ax.set_ylabel('Rating', fontsize=14, y= 1.05)
    plt.locator_params(axis="both", integer=True, tight=True)   
    ax.tick_params(labelsize=12)

    # Add legend
    ax.legend(['Ratings'])

    # Add title
    ax.set_title(f'Ratings throughout the years for {establishment_name}', fontsize=16)
    
    return [fig, list(zip(year, mean))]



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
            # TODOTAB: THIS IS FOR TESTING PURPOSES ONLY
            if start > 50:
                return all_reviews
        else:
            return all_reviews
        


def get_single_page_reviews(base_link, start):
    global establishment_name
    # Returns a list of reviews from a single page
    updated_link = base_link + "?start=" + str(start)
    r = requests.get(updated_link)
    soup = BeautifulSoup(r.text, "html.parser")
    establishment_name = soup.find("h1").text
    # div with an id of reviews with a child ul with a parital match class of list__ and it's children li
    single_page_reviews = soup.select("#reviews ul[class*='list__'] li") 
    return single_page_reviews if len(single_page_reviews) > 0 else False


def get_date_review_object(page_reviews_list, all_reviews):
    for review in page_reviews_list:
        # FIXME: Find a better way than hardcoding the date class
        date = review.find("span", {"class": "css-chan6m"}).text
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

def returnImageBase64(fig):
    # Save figure to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')

    # Convert to bytes 
    buf.seek(0)
    img_bytes = buf.read()

    # Encode bytes to base64 string 
    img_b64 = base64.b64encode(img_bytes).decode('utf8')

    # Return base64 string
    return img_b64

def get_plot(url):
    fig, graphValues = create_dataframe_and_plot(url)
    fig.savefig('plot+test.png')
    return [returnImageBase64(fig), graphValues]


if __name__ == "__main__":
    get_plot()


