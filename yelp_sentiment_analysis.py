# %%
import os
import re
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from bert_helpers import get_sentiment_score
from scraping_helpers import get_all_reviews_for_establishment

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fixes threads issue with matplotlib
import base64
import io


# def get_date_review_object(page_reviews_list, all_reviews):
#     for review in page_reviews_list:
#         date = review.find("span", {"class": "css-chan6m"}).text
#         comment = review.find("p", {"class": re.compile(".*comment.*")}).text.replace(
#             "\xa0", ""
#         )

#         # NLP can only work with tokens upto 512 characters
#         if len(comment) > 511:
#             n = 511
#             chunks = [[date, comment[i : i + n]] for i in range(0, len(comment), n)]
#             all_reviews.extend(chunks)
#         else:
#             all_reviews.append([date, comment])


def create_dataframe_and_plot(base_link):
    """
    Gets a list of review objects [[name, comment, date]]



    """
    all_reviews = get_all_reviews_for_establishment(base_link)
    print("AL REIVEWS length", len(all_reviews))
    establishment_name = all_reviews[0][2]

    reviews_for_df = [[review[0], review[1]] for review in all_reviews]
    print("reviews_for_df", len(reviews_for_df))
    df = pd.DataFrame(np.array(reviews_for_df), columns=["Date", "Comment"])

    print(df)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sentiment"] = df["Comment"].apply(lambda x: get_sentiment_score(x[:512]))
    df = df.sort_values("Date")
    df["Year"] = pd.DatetimeIndex(df["Date"]).year.astype(int)

    print("--------------------------")
    year_sentiment = df[["Year", "Sentiment"]].copy()
    df2 = year_sentiment.groupby("Year").aggregate(["mean", "count"])
    print(df2)
    year_mean_count_df = df2[df2.Sentiment["count"] > 5]
    year, mean = (
        year_mean_count_df["Sentiment"].index.astype(int),
        year_mean_count_df["Sentiment"]["mean"],
    )

    # Set plot style
    plt.style.use("seaborn")

    fig, ax = plt.subplots()

    # Plot line
    ax.plot(year, mean)
    ax.set_ylim(1, 5)

    # Axis aesthetics
    ax.grid(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Label aesthetics
    ax.set_xlabel("Years", fontsize=14, x=0.5, labelpad=10)
    ax.set_ylabel("Rating", fontsize=14, y=0.5, labelpad=10)
    plt.locator_params(axis="both", integer=True, tight=True)
    ax.tick_params(labelsize=12)

    # Add legend
    ax.legend(["Ratings"])

    # Add title
    ax.set_title(
        f"Ratings throughout the years for {establishment_name}", fontsize=16, pad=20
    )

    return [fig, list(zip(year, mean))]


def get_base64_from_fig(fig):
    # Save figure to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png")

    # Convert to bytes
    buf.seek(0)
    img_bytes = buf.read()

    # Encode bytes to base64 string
    img_b64 = base64.b64encode(img_bytes).decode("utf8")

    # Return base64 string
    return img_b64


def get_plot(url):
    figure, graph_values = create_dataframe_and_plot(url)
    print("graph_values", graph_values)
    figure.savefig("plot+test.png")
    return [get_base64_from_fig(figure), graph_values]


# TODOTAB: FIX TODO
# TEST_URL = "https://www.yelp.com/biz/bbq-nite-hicksville-3"
TEST_URL = "https://www.yelp.com/biz/fateh-s-bbq-east-meadow"


if __name__ == "__main__":
    get_plot(TEST_URL)
