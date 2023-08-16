"""
This Flask application provides endpoints for getting information about establishments based on yelp urls.
"""


from flask import Flask, request
from flask_cors import CORS

from open_ai_helpers import get_info_about_graphs
from yelp_sentiment_analysis import get_plot

app = Flask(__name__)
CORS(app, resources={r"/getDetails/*": {"origins": "http://localhost:3000"}})


@app.route("/", methods=["GET"])
def health_check():
    """
    A basic endpoint that returns a greeting message.
    """
    return "Hello to the World"


@app.route("/getDetails", methods=["GET"])
def get_details():
    """
    Endpoint for retrieving graph information.
    """
    status_code = 418

    try:
        second_url = request.args.get("url2")
        first_url = request.args.get("url1")
        base64_url1, graph_points_url1 = get_plot(first_url)
        base64_url2, graph_points_url2 = get_plot(second_url)
        status_code = 200

        gpt_blurb = get_info_about_graphs(graph_points_url1, graph_points_url2)

        response = {
            "data": {
                "url": first_url,
                "url1GraphImage": base64_url1,
                "url2GraphImage": base64_url2,
                "gptBlurb": gpt_blurb,
            }
        }

    except Exception as e:
        print("There was an error:", e)
        status_code = 500

        response = {
            "data": {
                "url": first_url,
                "graph": "There was an error",
            }
        }

    return response, status_code


if __name__ == "__main__":
    app.run(debug=True)
