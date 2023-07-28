import urllib.request
import requests
from bs4 import BeautifulSoup
import json

# url = "https://www.yelp.com/biz/Q9F2ocrmYuGt1yn3M7MOBw/review_feed?rl=en&q=&sort_by=relevance_desc&start=10"
# response = urllib.request.urlopen(url)
# full_response = response.read()
# json_data = json.loads(full_response)
# print(json_data["reviews"][0]["localizedDate"])
# print(json_data["reviews"][0]["comment"]["text"])
# print(json_data["reviews"][0]["business"]["name"])


def get_biz_id(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    biz_id = soup.find("meta", {"name": "yelp-biz-id"})["content"]
    return biz_id


def create_review_url_got_new_page(biz_id, start):
    return f"https://www.yelp.com/biz/{biz_id}/review_feed?rl=en&q=&sort_by=relevance_desc&start={start}"


def get_reviews_from_url(url):
    response = urllib.request.urlopen(url)
    full_response = response.read()
    json_data = json.loads(full_response)

    list_of_raw_review_objects = json_data["reviews"]

    res = []
    for reviewObj in list_of_raw_review_objects:
        date = reviewObj["localizedDate"]
        comment = reviewObj["comment"]["text"]
        name = reviewObj["business"]["name"]

        if len(comment) > 511:
            n = 511
            chunks = [
                [date, comment[i : i + n], name] for i in range(0, len(comment), n)
            ]
            res.extend(chunks)
        else:
            res.append([date, comment, name])

    return res


def get_all_reviews_for_establishment(base_yelp_url) -> list:
    """
    Returns a list of review objects for a given base url

    """
    biz_id = get_biz_id(base_yelp_url)
    start = 0
    all_reviews = []
    while True:
        review_url = create_review_url_got_new_page(biz_id, start)
        reviews_per_page = get_reviews_from_url(review_url)
        if reviews_per_page:
            all_reviews.extend(reviews_per_page)
            start += 10
            print(start)
            print(len(reviews_per_page))
            # TODOTAB: TESTING
            # if start > 500:
            # return all_reviews
        else:
            return all_reviews


# TEST_URL = "https://www.yelp.com/biz/lucali-brooklyn-3"
# print(get_all_reviews_for_establishment(TEST_URL)[0])
