import json
import urllib.request

import requests
from bs4 import BeautifulSoup

# Constants
MAX_COMMENT_LENGTH = 511
INCREMENT_VALUE = 10


def get_biz_id(url):
    """
    Extracts Yelp business ID from a given URL.
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        biz_id = soup.find("meta", {"name": "yelp-biz-id"})["content"]
        return biz_id
    except (requests.RequestException, KeyError, TypeError) as e:
        print(f"Error in get_biz_id: {e}")
        return None


def create_review_url(biz_id, start):
    """
    Creates a URL to retrieve reviews for a specific Yelp business and page.
    """
    return f"https://www.yelp.com/biz/{biz_id}/review_feed?rl=en&q=&sort_by=relevance_desc&start={start}"


def get_reviews_from_url(url):
    """
    Retrieves reviews from a given URL and processes them.
    """
    try:
        response = urllib.request.urlopen(url)
        full_response = response.read()
        json_data = json.loads(full_response)

        list_of_raw_review_objects = json_data.get("reviews", [])

        res = []
        for reviewObj in list_of_raw_review_objects:
            date = reviewObj["localizedDate"]
            comment = reviewObj["comment"]["text"]
            name = reviewObj["business"]["name"]

            if len(comment) > MAX_COMMENT_LENGTH:
                chunks = [
                    [date, comment[i : i + MAX_COMMENT_LENGTH], name]
                    for i in range(0, len(comment), MAX_COMMENT_LENGTH)
                ]
                res.extend(chunks)
            else:
                res.append([date, comment, name])

        return res
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error in get_reviews_from_url: {e}")
        return []


def get_all_reviews_for_establishment(business_url) -> list:
    """
    Retrieves all reviews for a given Yelp business URL.
    """
    try:
        biz_id = get_biz_id(business_url)
        if not biz_id:
            return []

        start = 0
        all_reviews = []
        while True:
            review_url = create_review_url(biz_id, start)
            reviews_per_page = get_reviews_from_url(review_url)
            if reviews_per_page:
                all_reviews.extend(reviews_per_page)
                start += INCREMENT_VALUE
            else:
                return all_reviews
    except Exception as e:
        print(f"Error in get_all_reviews_for_establishment: {e}")
        return []
